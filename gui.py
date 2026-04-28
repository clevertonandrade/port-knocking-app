import tkinter as tk
from tkinter import ttk, PhotoImage
import threading
import base64
import validators
import storage
import knocker

class PortKnockingApp:
    WINDOW_TITLE = "Port Knocking App"
    WINDOW_WIDTH = 320
    WINDOW_HEIGHT = 35 * 5
    PORT_ENTRY_HEIGHT = 35
    
    x_image = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAAiklEQVQ4y52TSw6AIAxEZyTxFB6KIxBDuP+OFdGF1SBKLXYJ8x6ftICUc26BsR5Zkh5AJrl+wSSjZH1tywA2AEWTCFwkm6+bCFQ0SQMXkqENdCUkkwprEjPckwzBHYkKTybjUfOf09snpCFYPjE0a9EMV3u6xNhI75LBVq4lt1YeGaaAepjO+jvOOzhaVK9oBnNvAAAAAElFTkSuQmCC"

    def __init__(self, root):
        self.root = root
        self.root.title(self.WINDOW_TITLE)

        # Configure a simple ttk theme to make it look a bit nicer
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.center_window()
        self.root.resizable(width=False, height=False)

        # Cache the remove image to avoid repeatedly decoding it
        remove_image_data = base64.b64decode(self.x_image)
        self.remove_photo_image = PhotoImage(data=remove_image_data)

        self.setup_ui()
        self.original_window_geometry = self.root.geometry()

    def center_window(self):
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x_coordinate = (screen_width - self.WINDOW_WIDTH) // 2
        y_coordinate = (screen_height - self.WINDOW_HEIGHT) // 2
        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x_coordinate}+{y_coordinate}")

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.setup_host_frame()
        self.setup_port_frame()
        self.setup_buttons()
        self.load_data()

    def setup_host_frame(self):
        self.host_frame = ttk.Frame(self.main_frame)
        self.host_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.host_frame, text="Host:").pack(side=tk.LEFT, padx=(0, 5))
        self.host_entry = ttk.Entry(self.host_frame, width=30)
        self.host_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def setup_port_frame(self):
        self.port_frame = ttk.Frame(self.main_frame)
        self.port_frame.pack(fill=tk.X, pady=5)

    def setup_buttons(self):
        self.add_port_button = ttk.Button(self.main_frame, text="Add Port", command=self.add_port)
        self.add_port_button.pack(pady=5)

        self.check_button = ttk.Button(self.main_frame, text="Perform Port Knocking", command=self.start_port_knocking)
        self.check_button.pack(pady=5)

        self.status_message = tk.Label(self.main_frame, text="", font=("Helvetica", 12))
        self.status_message.pack(pady=5)

    def add_port(self, port=None):
        new_port_frame = ttk.Frame(self.port_frame)
        new_port_frame.pack(fill=tk.X, pady=2)

        ttk.Label(new_port_frame, text="Port:").pack(side=tk.LEFT, padx=(0, 5))

        validate_port = self.root.register(self.validate_port_entry)
        new_port_entry = ttk.Entry(new_port_frame, width=20, validate="key", validatecommand=(validate_port, "%P"))
        new_port_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        if port:
            new_port_entry.insert(0, port)
    
        remove_button = ttk.Button(new_port_frame, image=self.remove_photo_image, command=lambda frame=new_port_frame: self.remove_port(frame), width=2)
        remove_button.pack(side=tk.RIGHT)

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
        remove_buttons = []
        for frame in self.port_frame.winfo_children():
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Button):
                    remove_buttons.append(widget)

        for button in remove_buttons:
            button["state"] = "disabled" if len(remove_buttons) == 1 else "normal"

    def start_port_knocking(self):
        host = self.host_entry.get()
        ports = []
        if self.port_frame.winfo_children():
            for frame in self.port_frame.winfo_children():
                for widget in frame.winfo_children():
                    if isinstance(widget, ttk.Entry) and widget.get():
                        ports.append(int(widget.get()))

        self.status_message.config(text="")

        if not any([validators.ipv4(host), validators.ipv6(host), validators.domain(host)]):
            self.status_message.config(text="\u2717 Invalid Host", fg="red")
            return

        if not ports:
            self.status_message.config(text="\u2717 No ports added", fg="red")
            return

        # Save data before knocking
        self.save_data()

        self.status_message.config(text="Knocking...", fg="blue")
        threading.Thread(target=self.perform_port_knocking_thread, args=(host, ports), daemon=True).start()

    def perform_port_knocking_thread(self, host, ports):
        success = knocker.perform_port_knocking(host, ports)

        # Schedule GUI update on the main thread
        self.root.after(0, self.update_status, success)

    def update_status(self, success):
        if success:
            self.status_message.config(text="\u2713 Port Knocking Successful", fg="green")
        else:
            self.status_message.config(text="\u2717 Port Knocking Failed", fg="red")

    def save_data(self):
        host = self.host_entry.get()
        ports = []
        for frame in self.port_frame.winfo_children():
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Entry):
                    ports.append(widget.get())
        storage.save_data(host, ports)

    def load_data(self):
        data = storage.load_data()

        self.host_entry.insert(0, data["host"])

        ports = data.get("ports", [""])
        if not ports:
            ports = [""]

        self.original_window_height = (len(ports) * 35) + self.WINDOW_HEIGHT

        for port in ports:
            self.add_port(port)

        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.original_window_height}")
        self.update_remove_button_state()

def run_app():
    root = tk.Tk()
    app = PortKnockingApp(root)
    root.mainloop()
