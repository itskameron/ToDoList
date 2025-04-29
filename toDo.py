"""
Author: Kameron Cole
Date Written: 4/25/2025
Assignment: Final Project
Short Desc: This application is an interactive To-Do List using GUI
"""

from breezypythongui import EasyFrame

class ToDo(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="What Needs Done")
        self.setSize(750, 750)

        # Create a list to store tasks
        self.tasks = []

        # Title Label
        self.addLabel(text="My To-Do List", row=0, column=0, columnspan=2)

        # Adds a text area for the task
        self.TaskArea = self.addTextArea(text="", row=1, column=0, columnspan=2)
        self.TaskArea["state"] = "disabled"

        # Adds a button to open text area
        self.addButton(text="Add Task", row=2, column=0, command=self.AddItem)

        # Makes a button to save the task
        self.SaveButton = self.addButton(text="Save Task", row=2, column=1, command=self.saveTask)
        self.SaveButton["state"] = "disabled"

    def AddItem(self):
        self.TaskArea["state"] = "normal"   # Allows user to add text
        self.TaskArea.setText("")            # Clears previous text
        self.SaveButton["state"] = "normal"  # Enables the Save button

    def saveTask(self):
        task = self.TaskArea.getText().strip()

        if task:  # Only save if there is text
            self.tasks.append(task)
            print("Saved Task:", task)
        else:
            print("No task entered.")

        # After saving, disable text area and Save button
        self.TaskArea.setText("")
        self.TaskArea["state"] = "disabled"
        self.SaveButton["state"] = "disabled"

def main():
    ToDo().mainloop()

if __name__ == "__main__":
    main()