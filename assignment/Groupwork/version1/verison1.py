import tkinter as tk
from PIL import Image, ImageTk, ImageSequence


class DesktopPet:
    def __init__(self, master):
        self.master = master
        self.master.title("Desktop Pet")

        self.master.overrideredirect(True)
        self.master.attributes("-transparentcolor", "gray")
        self.master.attributes("-topmost", True)

        try:
            self.normal_image = Image.open("normal.gif")  # Use only normal.gif
        except Exception as e:
            print(f"Error loading images: {e}")
            return

        self.is_normal_playing = True

        self.img_label = tk.Label(master, bg="gray")
        self.img_label.pack()

        self.normal_index = 0

        self.load_images()
        self.animate_normal()

        # Enable dragging of the window
        self.img_label.bind("<Button-1>", self.start_drag)
        self.img_label.bind("<B1-Motion>", self.do_drag)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_images(self):
        """Load and resize GIF frames"""
        self.normal_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(self.normal_image)]

    def animate_normal(self):
        """Animate normal"""
        if self.is_normal_playing:
            self.img_label.config(image=self.normal_frames[self.normal_index])
            self.normal_index = (self.normal_index + 1) % len(self.normal_frames)
        self.master.after(100, self.animate_normal)

    def start_drag(self, event):
        """Record initial mouse position for dragging"""
        self.last_x = event.x
        self.last_y = event.y

    def do_drag(self, event):
        """Drag the window"""
        x = self.master.winfo_x() - self.last_x + event.x
        y = self.master.winfo_y() - self.last_y + event.y
        self.master.geometry(f"+{x}+{y}")

    def on_closing(self):
        """Handle closing the window"""
        self.master.destroy()


root = tk.Tk()
pet = DesktopPet(root)
root.mainloop()
