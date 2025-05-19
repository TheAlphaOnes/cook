package prompt_ask

import (
	"fmt"

	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
)

// model defines the state of our application
type model struct {
	question  string
	textInput textinput.Model
	answer    string
}

// Init initializes the program
func (m model) Init() tea.Cmd {
	return textinput.Blink
}

// Update handles incoming messages and updates the model accordingly
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.Type {
		case tea.KeyEnter:
			// Store the user's input and exit
			m.answer = m.textInput.Value()
			return m, tea.Quit
		case tea.KeyCtrlC, tea.KeyEsc:
			// Exit without storing input
			return m, tea.Quit
		}
	}

	// Update the text input component
	var cmd tea.Cmd
	m.textInput, cmd = m.textInput.Update(msg)
	return m, cmd
}

// View renders the UI
func (m model) View() string {
	return fmt.Sprintf("%s\n\n%s\n\n(Press Enter to submit, Esc to cancel)", m.question, m.textInput.View())
}

// Ask prompts the user with a question and returns their input
func Ask(question string) (string, error) {
	ti := textinput.New()
	ti.Placeholder = "Type your answer..."
	ti.Focus()
	ti.CharLimit = 256
	ti.Width = 40

	m := model{
		question:  question,
		textInput: ti,
	}

	p := tea.NewProgram(m)
	finalModel, err := p.Run()
	if err != nil {
		return "", err
	}

	// Extract the answer from the final model
	return finalModel.(model).answer, nil
}

// func main() {
// 	answer, err := Ask("What's your favorite Pokémon?")
// 	if err != nil {
// 		log.Fatal(err)
// 	}
// 	fmt.Println("You answered:", answer)
// }
