""" 

Author: Kameron Cole 
Date Written: 4/25/2025 
Assignment: Final Project 
Short Desc: This application is an interactive To-Do List using GUI 
    
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage
from datetime import datetime


class ToDoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("What Needs Done")
        self.geometry("600x400")
        try:
            self.logo_image = PhotoImage(file="logo.png")
            logo_label = tk.label(self, image=self.logo_image)
            logo_label.place(x=10, y=10)
        except Exception as e:
            print("Logo not loaded:",)

        self.tasks = []
        self.load_tasks()

        nav_frame = tk.Frame(self)
        nav_frame.pack(pady=10)
        tk.Button(nav_frame, text="Add Task", command=self.show_add_task).pack(side="left", padx=10)
        tk.Button(nav_frame, text="View Tasks", command=self.show_view_tasks).pack(side="left", padx=10)

        # Add Task
        self.add_frame = tk.Frame(self)
        self.task_input = tk.Text(self.add_frame, height=3, width=50)
        self.task_input.pack(pady=5)
        tk.Label(self.add_frame, text="Priority (0 = Low, 1 = Medium, 2 = High):").pack()
        self.priority_var = tk.IntVar(value=0)
        self.priority_entry = tk.Spinbox(self.add_frame, from_=0, to=2, textvariable=self.priority_var)
        self.priority_entry.pack()
        self.save_button = tk.Button(self.add_frame, text="Save Task", command=self.save_task)
        self.save_button.pack(pady=5)

        # View Frame with Canvas and Scroll
        self.view_frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.view_frame)
        self.task_container = tk.Frame(self.canvas)
        self.scrollbar = tk.Scrollbar(self.view_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.task_container, anchor="nw")
        self.task_container.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.show_view_tasks()

        # Load and display footer image
        try:
            self.footer_image = PhotoImage(file="footer.png")
            footer_label = tk.Label(self, image=self.footer_image)
            footer_label.pack(side="bottom", pady=5)
        except Exception as e:
            print("Footer image not loaded:", e)

    def load_tasks(self):
        try:
            with open("data.txt", "r") as file:
                for line in file:
                    parts = line.strip().split("||")
                    if len(parts) == 3:
                        text, done, priority = parts
                    elif len(parts) == 2:
                        text, done = parts
                        priority = "0"
                    else:
                        text = parts[0]
                        done = "0"
                        priority = "0"
                    self.tasks.append({
                        "text": text,
                        "done": done == "1",
                        "priority": int(priority)
                    })
        except FileNotFoundError:
            self.tasks = []

    def save_all_tasks(self):
        with open("data.txt", "w") as file:
            for task in self.tasks:
                file.write(f"{task['text']}||{'1' if task['done'] else '0'}||{task['priority']}\n")

    def save_task(self):
        text = self.task_input.get("1.0", tk.END).strip()
        priority = self.priority_var.get()
        if text:
            self.tasks.append({"text": text, "done": False, "priority": priority})
            self.save_all_tasks()
            self.task_input.delete("1.0", tk.END)
            self.priority_var.set(0)
            messagebox.showinfo("Saved", "Task added successfully!")
            self.show_view_tasks()
        else:
            messagebox.showwarning("Empty", "Please enter a task.")

    def show_add_task(self):
        self.view_frame.pack_forget()
        self.add_frame.pack(pady=20)

    def show_view_tasks(self):
        self.add_frame.pack_forget()
        for widget in self.task_container.winfo_children():
            widget.destroy()

        # Sort tasks by priority (high first)
        sorted_tasks = sorted(self.tasks, key=lambda x: x["priority"], reverse=True)

        for idx, task in enumerate(sorted_tasks):
            self.create_task_widget(idx, task)

        self.view_frame.pack(fill="both", expand=True, pady=10)

    def show_view_tasks(self):
        self.add_frame.pack_forget()
        for widget in self.task_container.winfo_children():
            widget.destroy()

        sorted_tasks = sorted(self.tasks, key=lambda x: x["priority"], reverse=True)

        for task in sorted_tasks:
            self.create_task_widget(task)

        self.view_frame.pack(fill="both", expand=True, pady=10)

    def create_task_widget(self, task):
        frame = tk.Frame(self.task_container, pady=5)

        var = tk.BooleanVar(value=task["done"])
        checkbox = tk.Checkbutton(frame, variable=var, command=lambda t=task, v=var: self.toggle_done(t, v))
        checkbox.pack(side="left")

        priority_text = {0: "Low", 1: "Medium", 2: "High"}[task["priority"]]
        label = tk.Label(frame, text=f"[{priority_text}] {task['text']}", width=50,
                         anchor="w", fg="gray" if task["done"] else "black")
        label.pack(side="left", padx=5)

        tk.Button(frame, text="Edit", command=lambda t=task: self.edit_task(t)).pack(side="left", padx=5)
        tk.Button(frame, text="Delete", command=lambda t=task: self.delete_task(t)).pack(side="left")

        frame.pack(fill="x")

    def toggle_done(self, task, var):
        task["done"] = var.get()
        self.save_all_tasks()
        self.show_view_tasks()

    def edit_task(self, task):
        new_text = simpledialog.askstring("Edit Task", "Update task text:", initialvalue=task["text"])
        new_priority = simpledialog.askinteger("Edit Priority", "New priority (0=Low, 1=Medium, 2=High):",
                                               initialvalue=task["priority"], minvalue=0, maxvalue=2)
        if new_text is not None:
            task["text"] = new_text.strip()
        if new_priority is not None:
            task["priority"] = new_priority
        self.save_all_tasks()
        self.show_view_tasks()

    def delete_task(self, task):
        confirm = messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?")
        if confirm:
            self.tasks.remove(task)
            self.save_all_tasks()
            self.show_view_tasks()

if __name__ == "__main__":
    app = ToDoApp()
    app.mainloop()
