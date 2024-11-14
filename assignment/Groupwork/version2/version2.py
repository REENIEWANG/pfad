import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import math


class DesktopPet:
    def __init__(self, master):
        self.master = master
        self.master.title("Desktop Pet")

        self.master.overrideredirect(True)
        self.master.attributes("-transparentcolor", "gray")
        self.master.attributes("-topmost", True)

        try:
            self.normal_image = Image.open("D:/Term1/SD5913/Assignment/pfad/assignment/Groupwork/version2/normal.gif")
            self.icon_images = [
                Image.open("D:/Term1/SD5913/Assignment/pfad/assignment/Groupwork/version2/uialarm.png"),
                Image.open("D:/Term1/SD5913/Assignment/pfad/assignment/Groupwork/version2/uichat.png"),
                Image.open("D:/Term1/SD5913/Assignment/pfad/assignment/Groupwork/version2/uiexist.png"),
                Image.open("D:/Term1/SD5913/Assignment/pfad/assignment/Groupwork/version2/uiskin.png"),
                Image.open("D:/Term1/SD5913/Assignment/pfad/assignment/Groupwork/version2/uitouch.png"),
                Image.open("D:/Term1/SD5913/Assignment/pfad/assignment/Groupwork/version2/uizoom.png")
            ]
        except Exception as e:
            print(f"Error loading images: {e}")
            return

        self.is_normal_playing = True

        self.img_label = tk.Label(master, bg="gray")
        self.img_label.pack()

        self.normal_index = 0

        self.load_images()
        self.animate_normal()

        # 添加悬停功能
        self.hover_timer = None
        self.showing_icons = False

        # 功能图标的标签
        self.icon_labels = []
        for i in range(6):
            # 调整图标大小为 30x30
            icon_image = ImageTk.PhotoImage(self.icon_images[i].resize((30, 30)))
            icon_label = tk.Label(master, image=icon_image, bg="gray")
            icon_label.image = icon_image
            icon_label.place_forget()  # 初始隐藏
            self.icon_labels.append(icon_label)

        # 绑定鼠标悬停和离开的事件
        self.img_label.bind("<Enter>", self.on_hover)
        self.img_label.bind("<Leave>", self.on_leave)

        # 启用拖动窗口
        self.img_label.bind("<Button-1>", self.start_drag)
        self.img_label.bind("<B1-Motion>", self.do_drag)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_images(self):
        """加载和调整GIF帧"""
        self.normal_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(self.normal_image)]

    def animate_normal(self):
        """播放正常状态的动画"""
        if self.is_normal_playing:
            self.img_label.config(image=self.normal_frames[self.normal_index])
            self.normal_index = (self.normal_index + 1) % len(self.normal_frames)
        self.master.after(100, self.animate_normal)

    def start_drag(self, event):
        """记录初始鼠标位置以便拖动"""
        self.last_x = event.x
        self.last_y = event.y

    def do_drag(self, event):
        """拖动窗口"""
        x = self.master.winfo_x() - self.last_x + event.x
        y = self.master.winfo_y() - self.last_y + event.y
        self.master.geometry(f"+{x}+{y}")

    def on_closing(self):
        """关闭窗口"""
        self.master.destroy()

    def on_hover(self, event):
        """鼠标悬停事件"""
        if not self.showing_icons:
            self.hover_timer = self.master.after(2000, self.show_icons)  # 2秒后显示图标

    def on_leave(self, event):
        """鼠标移出事件"""
        if self.hover_timer:
            self.master.after_cancel(self.hover_timer)
            self.hover_timer = None
        self.hide_icons()

    def show_icons(self):
        """显示功能图标"""
        self.showing_icons = True
        center_x, center_y = self.master.winfo_width() // 2, self.master.winfo_height() // 2 + 30  # 下移中心点
        radius = 115  # 增大半径

        # 左侧三个图标
        left_angle_increment = 30  # 左边图标之间的角度增量（减小角度）
        for i in range(3):
            angle = math.radians(i * left_angle_increment - 30)  # 让左边图标以中间为中心，角度从-45度开始
            x = center_x + int(radius * math.cos(angle)) - 15 - 25  # 向左移10个像素
            y = center_y + int(radius * math.sin(angle)) - 15  # 调整图标大小为30x30，因此减去15
            self.icon_labels[i].place(x=x, y=y)

        # 右侧三个图标
        right_angle_increment = 30  # 右边图标之间的角度增量（减小角度）
        for i in range(3, 6):
            angle = math.radians((i - 3) * right_angle_increment + 150)  # 让右边图标以中间为中心，角度从135度开始
            x = center_x + int(radius * math.cos(angle)) - 15 + 15  # 向右移10个像素
            y = center_y + int(radius * math.sin(angle)) - 15  # 调整图标大小为30x30，因此减去15
            self.icon_labels[i].place(x=x, y=y)

    def hide_icons(self):
        """隐藏功能图标"""
        self.showing_icons = False
        for label in self.icon_labels:
            label.place_forget()


root = tk.Tk()
pet = DesktopPet(root)
root.mainloop()