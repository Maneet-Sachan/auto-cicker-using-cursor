import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import keyboard
import time
from threading import Thread
import os
from PIL import Image, ImageTk

def create_icon():
    # Create a simple icon if it doesn't exist
    if not os.path.exists("clicker_icon.ico"):
        # Create a 32x32 image with a mouse cursor
        img = Image.new('RGB', (32, 32), color='white')
        # Draw a simple mouse cursor
        pixels = img.load()
        for i in range(32):
            for j in range(32):
                if i < 16 and j < 16 and i + j < 16:
                    pixels[i, j] = (0, 0, 0)
        img.save("clicker_icon.ico")

class AutoClickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Set window icon
        try:
            self.root.iconbitmap("clicker_icon.ico")
        except:
            pass  # Ignore if icon setting fails
        
        # Variables
        self.clicking = False
        self.click_interval = tk.DoubleVar(value=0.1)
        self.mouse_x = tk.StringVar(value="0")
        self.mouse_y = tk.StringVar(value="0")
        self.running = True
        
        self.setup_gui()
        self.start_coordinate_tracker()
        
        # Bind F6 key
        keyboard.add_hotkey('F6', self.toggle_clicking)
        
    def setup_gui(self):
        # Style
        style = ttk.Style()
        style.configure("TButton", padding=10, font=('Helvetica', 10))
        style.configure("TLabel", font=('Helvetica', 10))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Auto Clicker", font=('Helvetica', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Mouse coordinates frame
        coord_frame = ttk.LabelFrame(main_frame, text="Mouse Coordinates", padding="10")
        coord_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(coord_frame, text="X:").grid(row=0, column=0, padx=5)
        ttk.Label(coord_frame, textvariable=self.mouse_x).grid(row=0, column=1, padx=5)
        ttk.Label(coord_frame, text="Y:").grid(row=0, column=2, padx=5)
        ttk.Label(coord_frame, textvariable=self.mouse_y).grid(row=0, column=3, padx=5)
        
        # Interval frame
        interval_frame = ttk.LabelFrame(main_frame, text="Click Interval", padding="10")
        interval_frame.pack(fill=tk.X, pady=10)
        
        interval_scale = ttk.Scale(
            interval_frame,
            from_=0.01,
            to=2.0,
            variable=self.click_interval,
            orient=tk.HORIZONTAL,
            length=300
        )
        interval_scale.pack(pady=5)
        
        interval_label = ttk.Label(
            interval_frame,
            textvariable=self.click_interval,
            font=('Helvetica', 10)
        )
        interval_label.pack()
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.start_button = ttk.Button(
            button_frame,
            text="Start (F6)",
            command=self.toggle_clicking,
            style="TButton"
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Status label
        self.status_label = ttk.Label(
            main_frame,
            text="Status: Stopped",
            font=('Helvetica', 10)
        )
        self.status_label.pack(pady=10)
        
        # Instructions
        instructions = """
Instructions:
• Press F6 or click Start to toggle clicking
• Adjust the slider to change click interval
• Current mouse coordinates are shown above
• Click interval: time between clicks in seconds
        """
        ttk.Label(main_frame, text=instructions, justify=tk.LEFT).pack(pady=10)
        
    def start_coordinate_tracker(self):
        def update_coordinates():
            while self.running:
                x, y = pyautogui.position()
                self.mouse_x.set(str(x))
                self.mouse_y.set(str(y))
                time.sleep(0.1)
        
        Thread(target=update_coordinates, daemon=True).start()
    
    def toggle_clicking(self):
        self.clicking = not self.clicking
        if self.clicking:
            self.status_label.config(text="Status: Running")
            self.start_button.config(text="Stop (F6)")
            Thread(target=self.click_loop, daemon=True).start()
        else:
            self.status_label.config(text="Status: Stopped")
            self.start_button.config(text="Start (F6)")
    
    def click_loop(self):
        while self.clicking:
            pyautogui.click()
            time.sleep(self.click_interval.get())
    
    def on_closing(self):
        self.running = False
        self.root.destroy()
        sys.exit()

def main():
    # Create icon first
    create_icon()
    
    # Start main application
    root = tk.Tk()
    app = AutoClickerGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 