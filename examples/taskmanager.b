#! define a Task class
class Task {
    #! methods
    str name
    str desc
    bool done

    #! initializer
    fn __init__ (class self, str name, str desc) -> {
        self.name = name
        self.desc = desc
        self.done = false
    }

    #! complete method
    fn complete (class self) -> {
        self.done = true
    }
}

#! vector of users
vec tasks[Task] = []

#! continuous loop
while true {
    #! print options
    out("[blue]1: Add task[/blue]")
    out("[blue]2: List tasks[/blue]")
    out("[blue]3: Mark task as completed[/blue]")

    #! take in choice
    int choice = toInt(inp("[1/2/3"))

    #! if choice is 1
    if choice == 1 {
        #! prompt for name and desc
        str prompt = inp("> ")
        str desc = inp("Desc: ")

        #! create a new task and append it to the vector
        Task newTask = new Task(prompt, desc)
        tasks.append(newTask)
    } 
    
    #! if choice is 2
    else if choice == 2 {
        #! print out all tasks
        for (int i = 0; i < tasks.length(); i++) {
            out(toStr(i + 1) + ": " + toStr(tasks[i]))
        }
    }

    #! if choice is 3
    else if choice == 3 {
        #! print out all tasks
        for (int i = 0; i < tasks.length(); i++) {
            out(toStr(tasks[i]))
        }
    }
}