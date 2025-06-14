import pyautogui
import keyboard
import time
import sys
from threading import Thread

class AutoClicker:
    def __init__(self):
        self.clicking = False
        self.click_interval = 0.1  # Default interval in seconds
        self.running = True  # New flag to control the main loop
        
    def toggle_clicking(self):
        self.clicking = not self.clicking
        if self.clicking:
            print("Auto Clicker Started!")
            print("Press F6 again to stop")
        else:
            print("Auto Clicker Stopped!")
    
    def click_loop(self):
        while self.running:  # Check the running flag
            if self.clicking:
                pyautogui.click()
                time.sleep(self.click_interval)
            time.sleep(0.01)  # Small delay to prevent high CPU usage
    
    def change_interval(self):
        try:
            new_interval = float(input("Enter new click interval in seconds (e.g., 0.1): "))
            if new_interval > 0:
                self.click_interval = new_interval
                print(f"Click interval set to {new_interval} seconds")
            else:
                print("Interval must be greater than 0")
        except ValueError:
            print("Please enter a valid number")
    
    def stop(self):
        self.clicking = False
        self.running = False
        print("Emergency Stop Activated!")
        print("Program will exit in 2 seconds...")
        time.sleep(2)
        sys.exit()

def main():
    print("Auto Clicker Started!")
    print("Press F6 to start/stop clicking")
    print("Press F7 to change click interval")
    print("Press F8 to exit")
    print("Emergency Stop: Press Ctrl + Q")
    
    auto_clicker = AutoClicker()
    
    # Start the clicking thread
    click_thread = Thread(target=auto_clicker.click_loop, daemon=True)
    click_thread.start()
    
    # Set up hotkeys
    keyboard.add_hotkey('F6', auto_clicker.toggle_clicking)
    keyboard.add_hotkey('F7', auto_clicker.change_interval)
    keyboard.add_hotkey('F8', auto_clicker.stop)
    keyboard.add_hotkey('ctrl+q', auto_clicker.stop)  # Emergency stop
    
    try:
        # Keep the main thread alive
        keyboard.wait()
    except KeyboardInterrupt:
        auto_clicker.stop()

if __name__ == "__main__":
    main() 