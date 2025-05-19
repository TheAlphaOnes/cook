package prompt_spin

import (
	"fmt"
	"time"

	"github.com/charmbracelet/bubbles/spinner"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

type model struct {
	spinner  spinner.Model
	message  string
	quitting bool
	quitChan chan struct{}
}

func newModel(msg string, quitChan chan struct{}) model {
	s := spinner.New()
	s.Spinner = spinner.Dot
	s.Style = lipgloss.NewStyle().Foreground(lipgloss.Color("205"))
	return model{
		spinner:  s,
		message:  msg,
		quitChan: quitChan,
	}
}

func (m model) Init() tea.Cmd {
	return m.spinner.Tick
}

func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	select {
	case <-m.quitChan:
		m.quitting = true
		return m, tea.Quit
	default:
	}

	var cmd tea.Cmd
	m.spinner, cmd = m.spinner.Update(msg)
	return m, cmd
}

func (m model) View() string {
	if m.quitting {
		return ""
	}
	return fmt.Sprintf("\n   %s %s\n", m.spinner.View(), m.message)
}

type Spinner struct {
	quitChan chan struct{}
	program  *tea.Program
}

// New creates a new Spinner
func New() *Spinner {
	return &Spinner{
		quitChan: make(chan struct{}),
	}
}

// Start begins the spinner with the given message
func (s *Spinner) Start(msg string) {
	m := newModel(msg, s.quitChan)
	s.program = tea.NewProgram(m, tea.WithoutSignalHandler(), tea.WithAltScreen())

	go func() {
		_, _ = s.program.Run()
	}()
}

// Stop stops the spinner safely
func (s *Spinner) Stop() {
	close(s.quitChan)
	time.Sleep(100 * time.Millisecond) // allow tea to clean up
}

// func main() {
// 	s := New()
// 	s.Start("Crunching numbers...")

// 	time.Sleep(3 * time.Second) // simulate work

// 	s.Stop()
// }
