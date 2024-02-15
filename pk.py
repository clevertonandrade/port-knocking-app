import tkinter as tk
from tkinter import PhotoImage
import socket
import json
import threading
import os
import base64
import validators

class PortKnockingApp:
    DATA_FOLDER = os.path.join(os.getenv("APPDATA"), "PortKnockingApp")
    DATA_FILE = os.path.join(DATA_FOLDER, "port_knocking_data.json")
    WINDOW_TITLE = "Port Knocking App"
    WINDOW_WIDTH = 300
    WINDOW_HEIGHT = 35 * 5
    PORT_ENTRY_HEIGHT = 35
    
    x_image = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAiklEQVQ4y52TSw6AIAxEZyTxFB6KIxBDuP+OFdGF1SBKLXYJ8x6ftICUc26BsR5Zkh5AJrl+wSSjZH1tywA2AEWTCFwkm6+bCFQ0SQMXkqENdCUkkwprEjPckwzBHYkKTybjUfOf09snpCFYPjE0a9EMV3u6xNhI75LBVq4lt1YeGaaAepjO+jvOOzhaVK9oBnNvAAAAAElFTkSuQmCC"

    def __init__(self, root):
        self.root = root
        self.root.title(self.WINDOW_TITLE)     
        self.center_window()
        self.root.resizable(width=False, height=False)

        self.setup_ui()
        self.original_window_geometry = self.root.geometry()

    def center_window(self):
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x_coordinate = (screen_width - self.WINDOW_WIDTH) // 2
        y_coordinate = (screen_height - self.WINDOW_HEIGHT) // 2
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")

    def setup_ui(self):
        self.setup_host_frame()
        self.setup_port_frame()
        self.setup_buttons()
        self.load_data()

    def setup_host_frame(self):
        self.host_frame = tk.Frame(self.root)
        self.host_frame.pack(pady=10)

        tk.Label(self.host_frame, text="Host:").grid(row=0, column=0)
        self.host_entry = tk.Entry(self.host_frame, width=30)
        self.host_entry.grid(row=0, column=1)

    def setup_port_frame(self):
        self.port_frame = tk.Frame(self.root)
        self.port_frame.pack(pady=10)

    def setup_buttons(self):
        self.add_port_button = tk.Button(self.root, text="Add Port", command=self.add_port)
        self.add_port_button.pack(pady=5)

        self.check_button = tk.Button(self.root, text="Perform Port Knocking", command=self.perform_port_knocking)
        self.check_button.pack(pady=5)

        self.status_message = tk.Label(self.root, text="", font=("Helvetica", 12), fg="black")
        self.status_message.pack(pady=5)

    def add_port(self, port=None):
        new_port_frame = tk.Frame(self.port_frame)
        new_port_frame.grid(sticky="ew", pady=5)

        tk.Label(new_port_frame, text="Port:").grid(row=0, column=0)

        validate_port = self.root.register(self.validate_port_entry)
        new_port_entry = tk.Entry(new_port_frame, width=30, validate="key", validatecommand=(validate_port, "%P"))
        new_port_entry.grid(row=0, column=1, padx=(0, 5))

        if port:
            new_port_entry.insert(0, port)
    
        remove_image_data = base64.b64decode(self.x_image)
        remove_image = PhotoImage(data=remove_image_data)
        remove_button = tk.Button(new_port_frame, image=remove_image, command=lambda frame=new_port_frame: self.remove_port(frame))
        remove_button.image = remove_image
        remove_button.grid(row=0, column=2, padx=(5, 0))

        self.status_message.config(text="")
        self.update_window_height("add")

    def validate_port_entry(self, value):
        if not value:
            return True
        try:
            return 1 <= int(value) <= 65535
        except ValueError:
            return False

    def remove_port(self, frame):
        frame.destroy()
        self.status_message.config(text="")
        self.update_window_height("remove")

    def update_window_height(self, change):
        current_height = self.root.winfo_height()
        new_height = current_height + self.PORT_ENTRY_HEIGHT if change == "add" else current_height - self.PORT_ENTRY_HEIGHT
        self.root.geometry(f"{self.WINDOW_WIDTH}x{new_height}")
        self.update_remove_button_state()

    def update_remove_button_state(self):
        remove_buttons = [button for frame in self.port_frame.winfo_children() for button in frame.winfo_children() if isinstance(button, tk.Button) and button.cget("image")]
        for button in remove_buttons:
            button["state"] = "disabled" if len(remove_buttons) == 1 else "normal"

    def perform_port_knocking(self):
        host = self.host_entry.get()
        ports = [int(entry.get()) for frame in self.port_frame.winfo_children() for entry in frame.winfo_children() if isinstance(entry, tk.Entry) and entry.get()] if self.port_frame.winfo_children() else []
        self.status_message.config(text="")

        if not any([validators.ipv4(host), validators.ipv6(host), validators.domain(host)]):
            self.status_message.config(text="\u2717 Invalid Host", fg="red")
            return

        if not ports:
            self.status_message.config(text="\u2717 No ports added", fg="red")
            return

        threading.Thread(target=self.perform_port_knocking_thread, args=(host, ports)).start()

    def perform_port_knocking_thread(self, host, ports):
        try:
            for port in ports:
                try:
                    socket.create_connection((host, port), timeout=0.01)
                except (socket.timeout):
                    continue 
            self.status_message.config(text="\u2713 Port Knocking Successful", fg="green")
        except Exception:
            self.status_message.config(text="\u2717 Port Knocking Failed", fg="red")

        self.save_data()

    def save_data(self):
        host = self.host_entry.get()
        ports = [entry.get() for frame in self.port_frame.winfo_children() for entry in frame.winfo_children() if isinstance(entry, tk.Entry)]
        data = {"host": host, "ports": ports}

        # Ensure the data folder exists
        os.makedirs(self.DATA_FOLDER, exist_ok=True)

        with open(self.DATA_FILE, "w") as file:
            json.dump(data, file)

    def load_data(self):
        try:
            with open(self.DATA_FILE, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"host": "", "ports": [""]}

        self.host_entry.insert(0, data["host"])
        self.original_window_height = (len(data["ports"]) * 35) + self.WINDOW_HEIGHT

        for port in data["ports"]:
            self.add_port(port)

        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.original_window_height}")
        self.update_remove_button_state()

if __name__ == "__main__":
    root = tk.Tk()
    app = PortKnockingApp(root)
    root.mainloop()
