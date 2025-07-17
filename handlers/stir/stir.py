import os
import time
import subprocess
import json
import threading
import signal
import socket
import fnmatch
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from handlers.pyprompt import Terminal
from handlers.const import DEFAULT_STIR_CONFIG
from handlers.stir.logger import log, Color, info, success, warning, error, debug

pyp = Terminal()

class StirMonitor:
    def __init__(self, command, watch_dir=".", ignore_patterns=None, watch_patterns=None, debug_mode=False, clean_mode=False):
        self.command = command
        self.watch_dir = watch_dir
        self.ignore_patterns = ignore_patterns or []
        self.watch_patterns = watch_patterns or ["*"]
        self.process = None
        self.restart_delay = 2
        self.last_restart = 0
        self.first_event = True
        self.debug_mode = debug_mode
        self.clean_mode = clean_mode
        
        # Setup event handler with pattern matching
        self.event_handler = PatternMatchingEventHandler(
            patterns=self.watch_patterns,
            ignore_patterns=self.ignore_patterns,
            ignore_directories=True,
            case_sensitive=True
        )
        
        # Bind event methods
        self.event_handler.on_modified = self._handle_event
        self.event_handler.on_created = self._handle_event
        self.event_handler.on_deleted = self._handle_event
        self.event_handler.on_moved = self._handle_event
        
    def _handle_event(self, event):
        """Handle file system events"""
        # Skip first event to prevent initial restart
        if self.first_event:
            self.first_event = False
            return
        
        # Additional ignore pattern matching (more flexible than PatternMatchingEventHandler)
        for ignore_pattern in self.ignore_patterns:
            if self._matches_pattern(event.src_path, ignore_pattern):
                if self.debug_mode:
                    debug(f"Ignoring change in {event.src_path}")
                return
        
        # Prevent rapid restarts
        current_time = time.time()
        if current_time - self.last_restart < self.restart_delay:
            return
        
        if not self.clean_mode:
            warning("restarting due to changes detected...")
            if self.debug_mode:
                debug(f"{event.event_type} {event.src_path}")
        
        self.restart_process()
        self.last_restart = current_time
    
    def _matches_pattern(self, path: str, pattern: str) -> bool:
        """Check if the given path matches the pattern using fnmatch"""
        return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(Path(path).name, pattern)
    
    def _is_port_free(self, port):
        """Check if a port is available"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return True
        except OSError:
            return False
    
    def start_process(self):
        """Start the development server"""
        try:
            if not self.clean_mode:
                success(f"Starting: {' '.join(self.command)}")
            
            # Create new process group to better manage child processes
            kwargs = {
                'stdout': subprocess.PIPE,
                'stderr': subprocess.PIPE,
                'universal_newlines': True,
                'bufsize': 1
            }
            
            # Add process group creation for Unix systems
            if os.name != 'nt':  # Not Windows
                kwargs['preexec_fn'] = os.setsid
            
            self.process = subprocess.Popen(self.command, **kwargs)
            
            # Print server output in real-time using separate threads
            if not self.clean_mode:
                def print_stdout():
                    if self.process and self.process.stdout:
                        try:
                            for line in iter(self.process.stdout.readline, ''):
                                if line:
                                    log(Color.BLUE, f"{line.rstrip()}")
                        except (ValueError, AttributeError):
                            # Stream closed or process ended
                            pass
                
                def print_stderr():
                    if self.process and self.process.stderr:
                        try:
                            for line in iter(self.process.stderr.readline, ''):
                                if line:
                                    error(f"ERROR: {line.rstrip()}")
                        except (ValueError, AttributeError):
                            # Stream closed or process ended
                            pass
                
                stdout_thread = threading.Thread(target=print_stdout, daemon=True)
                stderr_thread = threading.Thread(target=print_stderr, daemon=True)
                stdout_thread.start()
                stderr_thread.start()
                        
        except Exception as e:
            error(f"Error starting server: {e}")
    
    def stop_process(self):
        """Stop the development server"""
        if self.process and self.process.poll() is None:
            if not self.clean_mode:
                warning("Stopping server...")
            
            try:
                # Try to kill the process group first (for Unix systems)
                if os.name != 'nt' and hasattr(self.process, 'pid'):
                    try:
                        os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                        time.sleep(0.5)  # Give it time to terminate gracefully
                    except (ProcessLookupError, OSError):
                        pass
                
                # Terminate the main process
                self.process.terminate()
                self.process.wait(timeout=3)
                
            except subprocess.TimeoutExpired:
                if not self.clean_mode:
                    warning("Server didn't stop gracefully, forcing...")
                try:
                    # Force kill the process group
                    if os.name != 'nt' and hasattr(self.process, 'pid'):
                        try:
                            os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                        except (ProcessLookupError, OSError):
                            pass
                    
                    self.process.kill()
                    self.process.wait()
                except Exception as kill_error:
                    if not self.clean_mode:
                        error(f"Error force killing server: {kill_error}")
                    
            except Exception as e:
                if not self.clean_mode:
                    error(f"Error stopping server: {e}")
            finally:
                self.process = None
    
    def restart_process(self):
        """Restart the development server"""
        self.stop_process()
        
        # Wait for common ports to be freed
        #TODO: Need to optimize for faster restarts
        common_ports = [8080, 3000, 5000, 8000]
        for port in common_ports:
            for i in range(20):  # Try for 10 seconds
                if self._is_port_free(port):
                    break
                time.sleep(0.5)
            else:
                continue  # If port is still busy, continue to next port
            break  # If we found a free port, break out of the outer loop
        
        # Additional delay to ensure cleanup
        time.sleep(1)
        self.start_process()
    
    def start(self):
        """Start the monitor and observer"""
        if not self.clean_mode:
            # success("Universal Development Watcher Starting...")
            # info(f"Watching directory: {os.path.abspath(self.watch_dir)}")
            # info(f"Command: {' '.join(self.command)}")
            # info(f"Watching patterns: {', '.join(self.watch_patterns)}")
            
            if self.ignore_patterns:
                warning(f"Ignoring patterns: {', '.join(self.ignore_patterns)}")
            
            info("Enter 'rs' to restart or 'stop' to terminate")
            log(Color.CYAN, "=" * 50)
        
        # Start initial server
        self.start_process()
        
        # Setup file watcher
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.watch_dir, recursive=True)
        self.observer.start()
        
        # Interactive mode
        self._interactive_mode()
    
    def stop(self):
        """Stop the monitor and observer"""
        self.stop_process()
        
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()
        
        if not self.clean_mode:
            error("Terminated process")
    
    def _interactive_mode(self):
        """Handle interactive commands"""
        try:
            while True:
                try:
                    user_input = input().strip().lower()
                    if user_input == 'rs':
                        if not self.clean_mode:
                            info("Manual restart requested...")
                        self.restart_process()
                    elif user_input == 'stop':
                        break
                except EOFError:
                    break
        except KeyboardInterrupt:
            if not self.clean_mode:
                warning("\n Shutting down...")
        finally:
            self.stop()

# Configuration functions with colored output
def load_reload_config(config_file="reload.conf"):
    """Load reload configuration from JSON file"""
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            warning(f"Error reading {config_file}, will create new config")
            return {}
    return {}

def save_reload_config(config, config_file="reload.conf"):
    """Save reload configuration to JSON file"""
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        success(f"Configuration saved to {config_file}")
    except Exception as e:
        error(f"Error saving config: {e}")

def input_reload_config():
    """Ask user for reload configuration"""
    pyp.good("🔧 Setting up hot reload configuration...")
    
    config_data = DEFAULT_STIR_CONFIG.copy()
    
    # Ask for command to run
    command_str = pyp.ask("Enter the command to stir (e.g., 'npm run dev', 'go run main.go')", required=True)
    config_data['command'] = command_str.split()
    
    # Ask for watch patterns
    watch_patterns = pyp.ask_list("Enter patterns to watch (e.g., *.py, *.js, *.go) - leave empty for all files")
    config_data['watch_patterns'] = watch_patterns if watch_patterns else ["*"]
    
    # Ask for ignore patterns
    ignore_patterns = pyp.ask_list("Enter patterns to ignore (e.g., node_modules, .git, dist)")
    config_data['ignore_patterns'] = ignore_patterns if ignore_patterns else []
    
    # Ask for directory to watch
    config_data['watch_dir'] = pyp.choose_dir("Select directory to watch", default=".")
    
    # Ask for debug mode
    config_data['debug'] = pyp.confirm("Enable debug mode?", default=False)
    
    # Ask for clean mode
    config_data['clean'] = pyp.confirm("Enable clean mode (minimal output)?", default=False)
    
    pyp.good("Configuration will be saved to reload.conf")
    return config_data

def stir_hot_reload():
    """Function specifically for hot reload mode called from cmd.py"""
    success("Stir mode activated!")
    
    # Check if reload.conf exists
    reload_config_file = "reload.conf"
    if not os.path.exists(reload_config_file):
        # Ask user for configuration
        config = input_reload_config()
        save_reload_config(config, reload_config_file)
    else:
        # Load existing configuration
        config = load_reload_config(reload_config_file)
        if not config:
            # If config is empty or invalid, ask for new config
            config = input_reload_config()
            save_reload_config(config, reload_config_file)
        # else:
        #     success(f"Loaded configuration from {reload_config_file}")
    
    # Validate config
    if not config.get('command'):
        error("No command found in configuration!")
        return
    
    # Create and start monitor
    monitor = StirMonitor(
        command=config["command"],
        watch_dir=config.get("watch_dir", "."),
        ignore_patterns=config.get("ignore_patterns", []),
        watch_patterns=config.get("watch_patterns", ["*"]),
        debug_mode=config.get("debug", False),
        clean_mode=config.get("clean", False)
    )
    
    monitor.start()


