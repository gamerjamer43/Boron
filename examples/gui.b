#! A basic GUI application using borontk components
#import GUI

#! Create the main application window with a title and dimensions.
App app = new TkApplication("My GUI App", 800, 600)

#! Create a main panel with a light blue background and pack it to fill the window.
Panel mainPanel = new Panel(app, bg="lightblue")
mainPanel.pack(fill="both", expand=true)

#! Add a title label to the main panel.
Label lblTitle = new Label(mainPanel, text="Welcome to My GUI App")
lblTitle.pack(pady=10)  #! Use padding for spacing

#! Add a single-line text box to allow user input.
TextBox inputField = new TextBox(mainPanel)
inputField.pack(pady=10)

#! Define a callback function for the submit button.
#! This function retrieves text from the inputField and outputs it.
fn onSubmit() -> {
    str input = inputField.get()
    out("Submitted: " + input)
}

#! Create a button with the text "Submit" that calls the onSubmit function.
Button btnSubmit = new Button(mainPanel, text="Submit", command=onSubmit)
btnSubmit.pack(pady=10)

#! Run the GUI event loop to display the window and wait for user interaction.
app.run()