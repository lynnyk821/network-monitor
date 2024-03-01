import psutil
import tkinter as tk


class NetworkStats:
    def __init__(self):
        self.stats = []
        self.update_stats()

    def update_stats(self):
        id = -1
        network_stats = psutil.net_io_counters(pernic=True)
        for interface, stats in network_stats.items():
            id = id + 1
            self.stats.append({
                "Id": id,
                "Interface": interface,
                "Bytes Sent": stats.bytes_sent,
                "Bytes Received": stats.bytes_recv,
            })


class NetworkMonitor:
    columns = ("Id", "Interface", "Bytes Sent", "Bytes Received")

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Network Monitor")

        self.table_frame = tk.Frame(self.root)
        self.network_stats = NetworkStats().stats

        self.init_labels()
        self.init_table(self.network_stats)

        self.update_data()

    def init_labels(self):
        # self.main_label = tk.Label(self.root, text="Network Monitoring", font=("Helvetica", 12))
        # self.main_label.grid(row=0, column=0)

        self.cpu_label = tk.Label(self.root, text="CPU Usage:")
        self.cpu_label.grid(row=3, column=0)

        self.memory_label = tk.Label(self.root, text="Memory Usage:")
        self.memory_label.grid(row=4, column=0)

        self.disk_label = tk.Label(self.root, text="Disk data Usage:")
        self.disk_label.grid(row=5, column=0)

    def init_table(self, network_stats):
        self.table_frame.grid(row=1, column=0)

        for col, column_name in enumerate(self.columns):
            tk.Label(self.table_frame, text=column_name, relief=tk.FLAT, width=20, height=2).grid(row=0, column=col)

        for row, data in enumerate(network_stats, start=1):
            for col, key in enumerate(self.columns):
                tk.Label(self.table_frame, text=data[key], relief=tk.FLAT, width=30, height=2).grid(row=row, column=col)

    def update_data(self):
        # Network data
        self.network_stats = NetworkStats()
        self.init_table(self.network_stats.stats)
        # CPU data
        cpu_usage = psutil.cpu_percent()
        self.cpu_label.config(text=f"CPU Usage: {cpu_usage}%")
        # Memory data
        memory_usage = psutil.virtual_memory().percent
        self.memory_label.config(text=f"Memory Usage: {memory_usage}%")
        # Disk data
        disk_usage = psutil.disk_usage('/').percent
        self.disk_label.config(text=f"Disk Usage: {disk_usage}%")

        self.root.after(1500, self.update_data)

    def show(self):
        self.root.mainloop()