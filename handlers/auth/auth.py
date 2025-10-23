import os
from handlers import user
from handlers import backend
from handlers.pyprompt import Terminal

pyp = Terminal()


def login_with_key(key: str):
    """Login with a provided key directly."""
    try:
        spinerPyp = pyp.spinner("Logging in, please wait...")

        userData = backend.get_user_by_key(key).get("data")
        user.createUserData({
            "username": userData.get("username"),
            "name": userData.get("name"),
            "key": userData.get("connectionKey"),
            "email": userData.get("email"),
        })

        spinerPyp.ok("✓ Login successful!")
        pyp.good(f"Welcome back, {userData.get('name')}!")

    except Exception as e:
        spinerPyp.fail("✗ Login failed!")
        pyp.error(f"Invalid connection key or network error: {str(e)}")


def login():
    """Interactive login process."""
    isUser = user.validateUserData()

    if isUser:
        userData = user.readUserData()
        pyp.good(f"You are already logged in as {userData.get('name', 'Unknown')} ({userData.get('username', 'Unknown')})")

        if pyp.confirm("Do you want to login with a different account?"):
            logout()
        else:
            return

    try:
        pyp.show("Please enter your Cook connection key:")
        key = pyp.ask("Connection key", required=True)

        if not key.strip():
            pyp.error("Connection key cannot be empty.")
            return

        login_with_key(key)

    except KeyboardInterrupt:
        pyp.show("\nLogin cancelled by user.")
    except Exception as e:
        pyp.error(f"Login process failed: {str(e)}")


def logout():
    """Logout current user."""
    isUser = user.validateUserData()

    if not isUser:
        pyp.error("You are not logged in.")
        return

    try:
        userData = user.readUserData()
        username = userData.get('name', 'Unknown')

        if pyp.confirm(f"Are you sure you want to logout {username}?"):
            user.createUserData()  # Clear user data
            pyp.good("Successfully logged out!")
        else:
            pyp.show("Logout cancelled.")

    except Exception as e:
        pyp.error(f"Logout failed: {str(e)}")


def now():
    """Show current authentication status."""
    isUser = user.validateUserData()

    if not isUser:
        pyp.error("You are not logged in.")
        pyp.show("Use 'cook auth login' to authenticate.")
        return

    try:
        userData = user.readUserData()

        if not userData:
            pyp.error("Unable to read user data.")
            return

        # Format user data for display
        userDataList = []
        field_labels = {
            "name": "Full Name",
            "username": "Username",
            "email": "Email",
            "key": "Connection Key"
        }

        for key, value in userData.items():
            if key in field_labels:
                # Mask the connection key for security
                if key == "key" and value:
                    masked_key = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
                    userDataList.append({field_labels[key]: masked_key})
                else:
                    userDataList.append({field_labels[key]: value or "Not set"})

        pyp.display_form("Current User Information", userDataList)
        pyp.good("✓ Authentication verified")

    except Exception as e:
        pyp.error(f"Failed to retrieve user information: {str(e)}")
