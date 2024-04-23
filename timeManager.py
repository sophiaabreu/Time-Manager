import tkinter as tk  # Import tkinter module for GUI
from tkinter import messagebox  # Import messagebox for displaying alerts

class TaskBlock(tk.Frame):  # Define a class for displaying task blocks
    def __init__(self, master, text, priority, start_time, end_time, day, **kwargs):
        super().__init__(master, **kwargs)
        
        # Initialize attributes for task block
        self.priority = priority
        self.start_time = start_time
        self.end_time = end_time
        self.day = day
        
        # Create label for task name with specified text and background color based on priority
        self.text_label = tk.Label(self, text=text, width=20, anchor="w", bg=self.get_task_color(priority))
        self.text_label.pack(side=tk.TOP, fill=tk.X, expand=True)
        
        # Create label for task time with start and end time and background color based on priority
        self.time_label = tk.Label(self, text=f"{start_time} - {end_time}", width=20, bg=self.get_task_color(priority))
        self.time_label.pack(side=tk.TOP, fill=tk.X)
    
    def get_task_color(self, priority):  # Method to determine background color based on priority
        if priority == "High":
            return "pink"
        elif priority == "Medium":
            return "orange"
        else:
            return "light blue"

class GalacticTaskManager:  # Define main application class
    def __init__(self, root):  # Initialize main application
        self.root = root
        self.root.title("Galactic Task Manager")  # Set window title
        
        # Define days of the week
        self.days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Create frame for UI organization
        self.schedule_frame = tk.Frame(root)
        self.schedule_frame.pack(pady=10)
        
        # Create labels for days of the week
        for i, day in enumerate(self.days_of_week):
            label = tk.Label(self.schedule_frame, text=day, width=10)
            label.grid(row=0, column=i+1)
        
        # Dictionary to store tasks
        self.tasks = {day: [] for day in self.days_of_week}
        
        # Create button for adding tasks
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="light green")
        self.add_button.pack(pady=10, padx=20, side=tk.BOTTOM)
        
        # Create button for virtual assistant
        self.assistant_button = tk.Button(root, text="Virtual Assistant", command=self.virtual_assistant, bg="light blue")
        self.assistant_button.pack(pady=10, padx=20, side=tk.BOTTOM)

    def add_task(self):  # Method to add a task
        # Create a new task dialog window
        task_dialog = TaskDialog(self.root, self.days_of_week)
        self.root.wait_window(task_dialog.top)
        
        # If task data is provided, create a new task block
        if task_dialog.task_data:
            task_data = task_dialog.task_data
            # Check for overlapping tasks
            if self.check_for_overlaps(task_data):
                messagebox.showwarning("Warning", "Task overlaps with existing task. Please choose a different time.")
                return
            
            # Create a new task block and add it to the schedule frame
            task_block = TaskBlock(self.schedule_frame, text=task_data["text"], priority=task_data["priority"],
                                     start_time=task_data["start_time"], end_time=task_data["end_time"],
                                     day=task_data["day"], relief="ridge")
            task_block.grid(row=len(self.tasks[task_data["day"]])+2, column=self.days_of_week.index(task_data["day"])+1, sticky="ew")
            self.tasks[task_data["day"]].append(task_block)

    def check_for_overlaps(self, new_task_data):  # Method to check for overlapping tasks
        # Check if the new task overlaps with existing tasks
        day_tasks = self.tasks[new_task_data["day"]]
        for task in day_tasks:
            if (new_task_data["start_time"] < task.end_time) and (new_task_data["end_time"] > task.start_time):
                return True
        return False

    def virtual_assistant(self):  # Method to provide virtual assistant suggestions
        suggestions_window = tk.Toplevel(self.root)  # Create a new window for suggestions
        suggestions_window.title("Virtual Assistant Suggestions")  # Set window title
        suggestions_window.geometry("400x400")  # Set window size
        
        # Create text widget to display suggestions
        suggestions_text = tk.Text(suggestions_window, wrap=tk.WORD)
        suggestions_text.pack(fill=tk.BOTH, expand=True)

        # Provide suggestions on organizing the day
        suggestions = "Here are some suggestions to better organize your day:\n"
        for day, task_list in self.tasks.items():
            if task_list:
                tasks_sorted_by_start_time = sorted(task_list, key=lambda x: x.start_time)
                suggestions += f"\n{day}:\n"
                for task in tasks_sorted_by_start_time:
                    suggestions += f"- {task.text_label.cget('text')}: {task.start_time} - {task.end_time}\n"
        
        # Provide time optimization suggestions
        suggestions += "\nTime Optimization Suggestions:\n"
        for day, task_list in self.tasks.items():
            if task_list:
                optimized_tasks = self.optimize_day(task_list)
                suggestions += f"\n{day}:\n"
                for task in optimized_tasks:
                    suggestions += f"- {task.text_label.cget('text')}: {task.start_time} - {task.end_time}\n"

        suggestions_text.insert(tk.END, suggestions)  # Insert suggestions into text widget

    def optimize_day(self, tasks):  # Method to optimize tasks for the day
        optimized_tasks = []  # List to store optimized tasks

        # Sort tasks by start time
        sorted_tasks = sorted(tasks, key=lambda x: x.start_time)

        # Initialize start time as the beginning of the day
        current_time = "12:00 AM"

        for task in sorted_tasks:
            # If the task starts after the current time, add it to optimized_tasks
            if task.start_time >= current_time:
                optimized_tasks.append(task)
                current_time = task.end_time
        
        return optimized_tasks

class TaskDialog:  # Define a class for task dialog window
    def __init__(self, parent, days_of_week):
        self.top = tk.Toplevel(parent)  # Create a new window
        self.top.title("Add Task")  # Set window title
        
        self.task_data = {}  # Initialize task data dictionary
        
        # Widgets for task details
        tk.Label(self.top, text="Task:").grid(row=0, column=0, padx=5, pady=5)
        self.task_entry = tk.Entry(self.top, width=20)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.top, text="Priority:").grid(row=1, column=0, padx=5, pady=5)
        self.priority_var = tk.StringVar(self.top)
        self.priority_var.set("Low")  # Default priority
        self.priority_dropdown = tk.OptionMenu(self.top, self.priority_var, "Low", "Medium", "High")
        self.priority_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.top, text="Start Time:").grid(row=2, column=0, padx=5, pady=5)
        self.start_time_var = tk.StringVar(self.top)
        self.start_time_var.set("12:00 AM")  # Default start time
        self.start_time_dropdown = tk.OptionMenu(self.top, self.start_time_var, *self.get_time_options())
        self.start_time_dropdown.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(self.top, text="End Time:").grid(row=3, column=0, padx=5, pady=5)
        self.end_time_var = tk.StringVar(self.top)
        self.end_time_var.set("12:00 AM")  # Default end time
        self.end_time_dropdown = tk.OptionMenu(self.top, self.end_time_var, *self.get_time_options())
        self.end_time_dropdown.grid(row=3, column=1, padx=5, pady=5)
        
        # Dropdown for choosing day of the week
        tk.Label(self.top, text="Day:").grid(row=4, column=0, padx=5, pady=5)
        self.day_var = tk.StringVar(self.top)
        self.day_var.set(days_of_week[0])  # Default to Monday
        self.day_dropdown = tk.OptionMenu(self.top, self.day_var, *days_of_week)
        self.day_dropdown.grid(row=4, column=1, padx=5, pady=5)
        
        self.submit_button = tk.Button(self.top, text="Add", command=self.add_task)  # Button to add task
        self.submit_button.grid(row=5, columnspan=2, padx=5, pady=5)
    
    def add_task(self):  # Method to add task
        task = self.task_entry.get()  # Get task name
        priority = self.priority_var.get()  # Get task priority
        start_time = self.start_time_var.get()  # Get task start time
        end_time = self.end_time_var.get()  # Get task end time
        day = self.day_var.get()  # Get task day
        
        # Check if all fields are filled
        if task:
            # Store task data in task_data dictionary
            self.task_data = {"text": task, "priority": priority, "start_time": start_time, "end_time": end_time,
                              "day": day}
            self.top.destroy()  # Close task dialog window
        else:
            messagebox.showwarning("Warning", "Please fill in all fields.")  # Display warning if fields are not filled
    
    def get_time_options(self):  # Method to generate time options
        times = []
        for hour in range(24):
            for minute in range(0, 60, 30):
                times.append(f"{hour:02d}:{minute:02d} {'AM' if hour < 12 else 'PM'}")
        return times

if __name__ == "__main__":  # Entry point of the application
    root = tk.Tk()  # Create root window
    app = GalacticTaskManager(root)  # Initialize GalacticTaskManager instance
    root.mainloop()  # Run the application

