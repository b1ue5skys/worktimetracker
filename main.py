# Revision 0.52 1.11.2023

# slightly changes of the report function
# added current task duration (only works when switch task or start form paused doesn't function)

# todo: fix current task duration update label faliure

# todo: modularize the functions
    # todo: data (class)
        # todo: database for all days and entrys
        # todo: list of all seen references
    # todo: UI (tkinter)
        # todo: translate functions from this sheet (1)
        # todo: frontend function for adding entrys
        # todo: frontend function to edit entrys
        # todo: list of all entrys and durations (summarized)
    # todo: im- and export data incl. autosave and reload function (class)
        # todo: preferred format: csv load and write functions


import tkinter as tk
import UI

if __name__ == "__main__":

    # initialize the main window of the Tkinter application
    root = tk.Tk()
    # Create an instance of the WorkTimeTracker class (UI), passing the main window as an argument
    app = UI.WorkTimeTracker(root)
    # This line starts the Tkinter main event loop, allowing the application to run and respond to user events
    root.mainloop()
