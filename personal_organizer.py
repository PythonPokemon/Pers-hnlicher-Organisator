import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

class PersonalOrganizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Organizer")

        self.tasks = []

        self.load_tasks()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.add_task_tab()
        self.view_tasks_tab()

    def add_task_tab(self):
        add_tab = ttk.Frame(self.notebook)
        self.notebook.add(add_tab, text="Aufgabe hinzufügen")

        task_label = tk.Label(add_tab, text="Aufgabe:")
        task_label.pack(padx=10, pady=5)

        self.task_entry = tk.Entry(add_tab)
        self.task_entry.pack(padx=10, pady=5)

        date_label = tk.Label(add_tab, text="Datum (JJJJ-MM-TT HH:MM):")
        date_label.pack(padx=10, pady=5)

        self.date_entry = tk.Entry(add_tab)
        self.date_entry.pack(padx=10, pady=5)

        add_button = tk.Button(add_tab, text="Aufgabe hinzufügen", command=self.add_task)
        add_button.pack(padx=10, pady=5)

    def view_tasks_tab(self):
        view_tab = ttk.Frame(self.notebook)
        self.notebook.add(view_tab, text="Aufgaben anzeigen")

        self.task_listbox = tk.Listbox(view_tab)
        self.task_listbox.pack(padx=10, pady=5, fill="both", expand=True)

        view_button = tk.Button(view_tab, text="Aufgabe anzeigen", command=self.view_task)
        view_button.pack(padx=10, pady=5)

        self.task_content_text = tk.Text(view_tab, height=10, width=40)
        self.task_content_text.pack(padx=10, pady=5)

        self.update_task_listbox()

    def add_task(self):
        task = self.task_entry.get()
        date_str = self.date_entry.get()
        
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            self.tasks.append({"task": task, "date": date_obj})
            messagebox.showinfo("Erfolg", "Aufgabe hinzugefügt.")
            self.task_entry.delete(0, "end")
            self.date_entry.delete(0, "end")
            self.update_task_listbox()
        except ValueError:
            messagebox.showerror("Fehler", "Ungültiges Datumsformat. Verwenden Sie JJJJ-MM-TT HH:MM.")

    def view_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            selected_task_index = selected_task_index[0]
            task_info = self.tasks[selected_task_index]
            self.task_content_text.delete("1.0", "end")
            self.task_content_text.insert("1.0", f"Aufgabe: {task_info['task']}\nDatum: {task_info['date']}")
        else:
            messagebox.showwarning("Fehler", "Bitte wählen Sie eine Aufgabe aus der Liste aus.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task_info in self.tasks:
            self.task_listbox.insert(tk.END, task_info["task"])

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file)
        messagebox.showinfo("Erfolg", "Aufgaben gespeichert.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalOrganizer(root)
    root.protocol("WM_DELETE_WINDOW", app.save_tasks)
    root.mainloop()
