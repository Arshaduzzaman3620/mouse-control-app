import tkinter as tk
from tkinter import messagebox
import pyautogui
import time

class AreaSelector:
    def __init__(self):
        self.selected_areas = []
        self.is_selecting = True
        self.selection_window_open = False

    def on_mouse_down(self, event):
        if self.is_selecting:
            self.start_x = event.x
            self.start_y = event.y

    def on_mouse_drag(self, event):
        if self.is_selecting:
            self.end_x = event.x
            self.end_y = event.y
            self.canvas.delete("rect")
            self.canvas.create_rectangle(self.start_x, self.start_y, self.end_x, self.end_y, outline='red', tag="rect")

    def on_mouse_up(self, event):
        if self.is_selecting:
            self.end_x = event.x
            self.end_y = event.y
            self.selected_areas.append((self.start_x, self.start_y, self.end_x, self.end_y))
            if len(self.selected_areas) < 3:
                messagebox.showinfo("Area Selected", f"Selected area from ({self.start_x}, {self.start_y}) to ({self.end_x}, {self.end_y})")
            if len(self.selected_areas) >= 3:
                self.is_selecting = False
                self.close_selection_window()

    def start_selection(self):
        self.selected_areas = []
        self.is_selecting = True
        self.selection_window_open = True

        # Create a new window for selection
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)  # Fullscreen window
        self.root.attributes("-alpha", 0.3)  # Semi-transparent window
        self.root.title("Select Area")

        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)

        # Add a reset button to clear the selection
        reset_button = tk.Button(self.root, text="Reset Selection", command=self.reset_selection)
        reset_button.pack()

        self.root.mainloop()

    def close_selection_window(self):
        if self.selection_window_open:
            self.selection_window_open = False
            self.root.quit()
            self.root.destroy()

    def reset_selection(self):
        # Clear the selected areas without hanging the application
        self.selected_areas = []
        self.canvas.delete("rect")  # Remove any drawn rectangle
        messagebox.showinfo("Selection Reset", "All selections have been reset. You can select again.")

    def click_selected_areas(self):
        if not self.selected_areas:
            messagebox.showinfo("Error", "No areas selected!")
            return

        clicked_areas = []  # To avoid double-clicking
        for area in self.selected_areas:
            x = (area[0] + area[2]) // 2  # Center of the selected area
            y = (area[1] + area[3]) // 2
            if (x, y) not in clicked_areas:
                pyautogui.moveTo(x, y, duration=0.5)  # Smooth movement
                pyautogui.click()
                clicked_areas.append((x, y))  # Mark this area as clicked
                time.sleep(1)  # Delay between clicks

        # Provide feedback after all clicks are done
        messagebox.showinfo("Clicking Complete", "All selected areas have been clicked.")

# Main function to run the app
def main():
    selector = AreaSelector()
    
    root = tk.Tk()
    root.title("Mouse Control App")
    root.geometry("300x200")

    # Button to open the selection overlay
    select_button = tk.Button(root, text="Select Area", command=selector.start_selection)
    select_button.pack(pady=20)

    # Button to start clicking the selected areas
    click_button = tk.Button(root, text="Click Selected Areas", command=selector.click_selected_areas)
    click_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
