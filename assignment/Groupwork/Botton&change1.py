import tkinter as tk
from PIL import Image, ImageTk, ImageSequence


class DesktopPet:
    def __init__(self, master, button_width=80, button_height=30):
        self.master = master
        self.master.title("Desktop Pet")

        # 去掉窗口边框
        self.master.overrideredirect(True)

        # 设置窗口背景为透明
        self.master.attributes("-transparentcolor", "gray")

        # 设置窗口总在最上层
        self.master.attributes("-topmost", True)

        # 加载图片
        try:
            self.gif1_image = Image.open("gif1.gif")
            self.gif2_image = Image.open("gif2.gif")
            self.button_image = Image.open("button.jpg")
        except Exception as e:
            print(f"Error loading images: {e}")
            return

        # 初始缩放因子
        self.scale_factor = 1.0

        # 创建标签显示 GIF
        self.img_label = tk.Label(master, bg="gray")
        self.img_label.pack()

        # 创建按钮，点击时切换 GIF
        self.button = tk.Button(master, command=self.switch_gif, borderwidth=0, bg="gray")
        self.button.place(x=10, y=10)

        # 缩放按钮
        self.scale_up_button = tk.Button(master, text="+", command=self.scale_up, width=button_width,
                                          height=button_height)
        self.scale_up_button.place(x=10, y=80)

        self.scale_down_button = tk.Button(master, text="_", command=self.scale_down, width=button_width,
                                            height=button_height)
        self.scale_down_button.place(x=10, y=120)

        # 初始化索引
        self.gif1_index = 0
        self.gif2_index = 0
        self.is_gif1_playing = True

        self.load_images()  # 加载图像
        self.animate_gif1()  # 开始播放 gif1

        # 允许拖动
        self.img_label.bind("<Button-1>", self.start_drag)
        self.img_label.bind("<B1-Motion>", self.do_drag)

        # 处理关闭事件
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_images(self):
        # 加载 GIF 框架
        self.gif1_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA").resize(
            (int(frame.width * self.scale_factor), int(frame.height * self.scale_factor)))) for frame in
                            ImageSequence.Iterator(self.gif1_image)]
        self.gif2_frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA").resize(
            (int(frame.width * self.scale_factor), int(frame.height * self.scale_factor)))) for frame in
                            ImageSequence.Iterator(self.gif2_image)]
        self.update_button_image()

    def update_button_image(self):
        # 更新按钮图像
        resized_button_image = self.button_image.convert("RGBA").resize(
            (int(self.button_image.width * self.scale_factor), int(self.button_image.height * self.scale_factor)))
        self.button_img = ImageTk.PhotoImage(resized_button_image)
        self.button.config(image=self.button_img)  # 更新按钮图像

    def animate_gif1(self):
        if self.is_gif1_playing:
            self.img_label.config(image=self.gif1_frames[self.gif1_index])
            self.gif1_index = (self.gif1_index + 1) % len(self.gif1_frames)
        self.master.after(100, self.animate_gif1)

    def animate_gif2(self):
        if not self.is_gif1_playing:  # 检查 gif1 是否没有播放
            self.img_label.config(image=self.gif2_frames[self.gif2_index])  # 更新图像为 gif2 的当前帧
            self.gif2_index = (self.gif2_index + 1) % len(self.gif2_frames)  # 更新索引
        self.master.after(100, self.animate_gif2)  # 设置下次调用

    def switch_gif(self):
        self.is_gif1_playing = False
        self.gif2_index = 0
        self.animate_gif2()
        self.master.after(30000, self.switch_back)

    def switch_back(self):
        self.is_gif1_playing = True
        self.gif1_index = 0  # 重置 gif1 的索引
        self.img_label.config(image=self.gif1_frames[self.gif1_index])  # 显示 gif1
        self.animate_gif1()  # 开始播放 gif1

    def start_drag(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def do_drag(self, event):
        x = self.master.winfo_x() - self.last_x + event.x
        y = self.master.winfo_y() - self.last_y + event.y
        self.master.geometry(f"+{x}+{y}")

    def scale_up(self):
        self.scale_factor *= 1.1  # 放大10%
        self.update_images()

    def scale_down(self):
        self.scale_factor /= 1.1  # 缩小10%
        self.update_images()

    def update_images(self):
        self.load_images()  # 重新加载图像以更新尺寸
        if self.is_gif1_playing:
            self.img_label.config(image=self.gif1_frames[self.gif1_index])  # 更新当前显示的图像
        else:
            self.img_label.config(image=self.gif2_frames[self.gif2_index])

    def on_closing(self):
        self.master.destroy()  # 销毁窗口，结束程序


# 创建主窗口
root = tk.Tk()
pet = DesktopPet(root, button_width=5, button_height=2)  # 在这里自定义按钮大小
root.mainloop()




