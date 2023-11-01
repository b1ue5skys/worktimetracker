import tkinter as tk
from tkinter import simpledialog
import time
import datetime
import csv
from collections import defaultdict

FONT = "JetBrains Mono"

class WorkTimeTracker:
    def __init__(self, master):
        self.master = master
        master.title("Work Time Tracker")
        self.timer = None
        self.current_task_start_time = None
        self.start_time = None
        self.total_time = 0
        self.work_data = []
        self.is_paused = True

        # Interval for Backup
        self.backup_interval = 600000  # 10 minutes in milliseconds

        # UI Elements

        self.label = tk.Label(master, text="Time Delta to 8 Hours: 08:00:00", font=(FONT, 16), padx=10, pady=5)
        self.label.pack()

        self.current_task_duration_label = tk.Label(master, text="Current Task Duration: 00:00:00", font=(FONT, 16),
                                                    padx=10, pady=5)
        self.current_task_duration_label.pack()

        self.task_label = tk.Label(master, text="Current Task: None", font=(FONT, 16), padx=10, pady=5)
        self.task_label.pack()

        self.start_pause_button = tk.Button(master, text="Start", command=self.toggle_start_pause, height=2, width=20, font=(FONT, 14))
        self.start_pause_button.pack()

        self.switch_button = tk.Button(master, text="Switch Task", command=self.switch_task, height=2, width=20, font=(FONT, 14))
        self.switch_button.pack()

        self.report_button = tk.Button(master, text="Generate Report", command=self.generate_report, height=2, width=20, font=(FONT, 14))
        self.report_button.pack()

        self.master.after(self.backup_interval, self.backup)

    def toggle_start_pause(self):
        if self.is_paused:
            self.start_pause_button.config(text="Pause")
            self.start_task()
            self.is_paused = False
        else:
            self.start_pause_button.config(text="Start")
            self.pause_task()
            self.is_paused = True

    def start_task(self):
        reference = simpledialog.askstring("Input", "Enter the reference:")
        task_description = simpledialog.askstring("Input", "Enter the task description:")
        self.start_time = time.time()
        self.current_task_start_time = time.time()
        self.work_data.append({'reference': reference, 'task_description': task_description, 'start_time': self.start_time, 'end_time': None})
        self.task_label.config(text=f"Current Task: {task_description} (Reference: {reference})")
        self.start_timer()
        self.update_current_task_duration()

    def pause_task(self):
        end_time = time.time()
        self.total_time += end_time - self.start_time
        self.work_data[-1]['end_time'] = end_time
        self.update_time_label()
        self.stop_timer()
        self.task_label.config(text="Current Task: None")
        self.update_current_task_duration()

    def switch_task(self):
        if not self.is_paused:
            self.pause_task()
            self.start_task()

    def start_timer(self):
        if self.timer is not None:
            self.stop_timer()
        self.timer = self.master.after(1000, self.update_timer)

    def stop_timer(self):
        if self.timer is not None:
            self.master.after_cancel(self.timer)
            self.timer = None

    def update_timer(self):
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        self.total_time += elapsed_time
        self.start_time = current_time
        self.update_time_label()
        self.timer = self.master.after(1000, self.update_timer)

    def update_current_task_duration(self):
        if self.current_task_start_time is not None and not self.is_paused:
            elapsed_time = time.time() - self.current_task_start_time
            formatted_time = str(datetime.timedelta(seconds=int(elapsed_time)))
            self.current_task_duration_label.config(text=f"Current Task Duration: {formatted_time}")
            self.master.after(1000, self.update_current_task_duration)
        else:
            self.current_task_duration_label.config(text="Current Task Duration: 00:00:00")

    def update_time_label(self):
        # Updates the time label in the GUI
        delta_to_eight_hours = (8 * 3600) - self.total_time
        if delta_to_eight_hours > 0:
            self.label.config(text=f"Time Delta to 8 Hours: {datetime.timedelta(seconds=int(delta_to_eight_hours))}")
        else:
            self.label.config(text=f"Total Worked Time: {datetime.timedelta(seconds=int(self.total_time))}")

    def generate_report(self):
        report_data = []
        reference_summary = defaultdict(lambda: {'duration': 0, 'tasks': []})

        for task in self.work_data:
            start_time = datetime.datetime.fromtimestamp(task['start_time']).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.fromtimestamp(task['end_time']).strftime('%Y-%m-%d %H:%M:%S') if task['end_time'] else 'Ongoing'
            duration = datetime.timedelta(seconds=task['end_time'] - task['start_time']) if task['end_time'] else 'Ongoing'
            reference_summary[task['reference']]['duration'] += task['end_time'] - task['start_time'] if task['end_time'] else 0
            reference_summary[task['reference']]['tasks'].append(task['task_description'])

            report_data.append({
                'Reference': task['reference'],
                'Start': start_time,
                'End': end_time,
                'Duration': str(duration),
                'Task': task['task_description']
            })

        with open('report.txt', 'w') as file:
            # Write tasks
            for data in report_data:
                file.write(f"Reference: {data['Reference']}, Start: {data['Start']}, End: {data['End']}, Duration: {data['Duration']}, Task: {data['Task']}\n")

            # Write summary
            file.write("\nSummary:\n")
            for reference, summary in reference_summary.items():
                file.write(f"Reference: {reference}, Total Duration: {datetime.timedelta(seconds=summary['duration'])}\n")
                for task in summary['tasks']:
                    file.write(f"  Task: {task}\n")

        print("Report generated!")

    def backup(self):
        # Saves work data to a CSV file
        with open('work_data.csv', 'w', newline='') as csvfile:
            fieldnames = ['reference', 'task_description', 'start_time', 'end_time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in self.work_data:
                writer.writerow(row)

        self.master.after(self.backup_interval, self.backup)