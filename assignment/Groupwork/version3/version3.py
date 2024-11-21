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
            # 加载初始皮肤 GIF 和备用皮肤 GIF
            self.normal_image = Image.open("data1/normal.gif")
            self.default_image = Image.open("data1/normal.gif")  # 默认皮肤
            self.alternate_image = Image.open("data1/skin/normal2.gif")
            self.icon_images = [
                Image.open("data1/uialarm.png"),
                Image.open("data1/uitouch.png"),
                Image.open("data1/uichat.png"),
                Image.open("data1/uizoom.png"),
                Image.open("data1/uiskin.png"),
                Image.open("data1/uiexist.png")
            ]
            # 加载手形光标图像
            self.hand_cursor_image = Image.open("data1/hand.png")
            self.hand_cursor = ImageTk.PhotoImage(self.hand_cursor_image.resize((30, 30)))

            # 加载表情框图片
            self.emotion_images = {
                "happy": ImageTk.PhotoImage(Image.open("data1/uikuang_happy.png")),
                "sad": ImageTk.PhotoImage(Image.open("data1/uikuang_sad.png")),
                "angry": ImageTk.PhotoImage(Image.open("data1/uikuang_angry.png")),
                "bored": ImageTk.PhotoImage(Image.open("data1/uikuang_bored.png"))
            }

        except Exception as e:
            print(f"Error loading images: {e}")
            return

        self.is_normal_playing = True
        self.is_alternate_skin = False  # 默认皮肤标志
        self.scale_factor = 1.0  # 初始缩放倍数

        self.img_label = tk.Label(master, bg="gray")
        self.img_label.pack()

        self.normal_index = 0

        self.load_images()  # 加载默认皮肤
        self.animate_normal()  # 启动默认皮肤动画

        # 初始化时将 original_image 设置为 normal_image
        self.original_image = self.normal_image

        # 添加悬停功能
        self.hover_timer = None
        self.showing_icons = False
        self.original_cursor = self.master["cursor"]  # 存储原始光标

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

        # 初始化情绪显示
        self.emotion_label = tk.Label(master, bg="gray")
        self.emotion_label.place_forget()  # 初始隐藏

    def load_images(self):
        """加载和调整当前皮肤 GIF 帧，应用当前缩放倍数"""
        image = self.alternate_image if self.is_alternate_skin else self.normal_image
        # 根据缩放倍数调整每帧大小
        self.normal_frames = [
            ImageTk.PhotoImage(
                frame.copy().convert("RGBA").resize(
                    (int(frame.width * self.scale_factor), int(frame.height * self.scale_factor))
                )
            ) for frame in ImageSequence.Iterator(image)
        ]
        # 更新当前帧显示
        if self.normal_frames:
            self.img_label.config(image=self.normal_frames[0])

    def animate_normal(self):
        """播放当前皮肤状态的动画"""
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
        self.hide_timer = self.master.after(3000, self.hide_icons)  # 延迟3秒后隐藏图标

    def show_icons(self):
        """显示功能图标"""
        if self.hide_timer:
            self.master.after_cancel(self.hide_timer)
            self.hide_timer = None

        self.showing_icons = True
        center_x, center_y = self.master.winfo_width() // 2, self.master.winfo_height() // 2 + 30  # 下移中心点
        radius = 115  # 增大半径

        # 左侧三个图标
        left_angle_increment = 30  # 左边图标之间的角度增量
        for i in range(3):
            angle = math.radians(i * left_angle_increment - 30)
            x = center_x + int(radius * math.cos(angle)) - 15 - 25  # 向左移10个像素
            y = center_y + int(radius * math.sin(angle)) - 15  # 调整图标大小为30x30
            self.icon_labels[i].place(x=x, y=y)
            self.icon_labels[i].bind("<Button-1>", lambda e, idx=i: self.icon_action(idx))

        # 右侧三个图标
        right_angle_increment = 30  # 右边图标之间的角度增量
        for i in range(3, 6):
            angle = math.radians((i - 3) * right_angle_increment + 150)
            x = center_x + int(radius * math.cos(angle)) - 15 + 15  # 向右移10个像素
            y = center_y + int(radius * math.sin(angle)) - 15  # 调整图标大小为30x30
            self.icon_labels[i].place(x=x, y=y)
            self.icon_labels[i].bind("<Button-1>", lambda e, idx=i: self.icon_action(idx))

    def hide_icons(self):
        """隐藏功能图标"""
        self.showing_icons = False
        for label in self.icon_labels:
            label.place_forget()

    def icon_action(self, idx):
        """处理每个图标的单独点击功能"""
        if idx == 0:
            print("功能1：显示闹钟")
        elif idx == 1:
            print("功能2：触摸反应")
            self.set_touch_reaction()  # 设置触摸反应
        elif idx == 2:
            print("功能3：聊天窗口")
            self.show_emotion_options()  # 显示情绪选项
        elif idx == 3:
            self.zoom_in()
            self.icon_labels[idx].bind("<Button-3>", lambda e: self.zoom_out())
        elif idx == 4:
            self.switch_skin()
        elif idx == 5:
            self.on_closing()

    def show_emotion_options(self):
        """显示聊天选项（开心，伤心，生气，无聊）"""
        options = ["happy", "sad", "angry", "bored"]
        for i, emotion in enumerate(options):
            btn = tk.Button(self.master, text=emotion.capitalize(), command=lambda e=emotion: self.show_emotion(e))
            btn.place(x=10 + i * 80, y=10)  # 调整按钮位置
            self.master.after(2000, btn.destroy)  # 延迟2秒后自动销毁选项按钮

    def show_emotion(self, emotion):
        """显示选中情绪的图像"""
        self.original_image = self.normal_image  # 保存当前皮肤（无论是否为原皮肤）

        if emotion == "happy":
            # 加载并显示 happy.gif 作为新的皮肤
            self.normal_image = Image.open("data1/happy.gif")
            self.load_images()  # 重新加载图像
            self.normal_index = 0
            self.img_label.config(image=self.normal_frames[self.normal_index])

            # 显示情绪框，显示为 'happy' 情绪
            self.emotion_label.config(image=self.emotion_images["happy"])
            self.emotion_label.place(x=75, y=50)  # 表情框位置

        elif emotion == "sad":
            # 加载并显示 sad.gif 作为新的皮肤
            self.normal_image = Image.open("data1/sad.gif")
            self.load_images()  # 重新加载图像
            self.normal_index = 0
            self.img_label.config(image=self.normal_frames[self.normal_index])

            # 显示情绪框，显示为 'sad' 情绪
            self.emotion_label.config(image=self.emotion_images["sad"])
            self.emotion_label.place(x=75, y=50)  # 表情框位置

        elif emotion == "angry":
            # 加载并显示 angry.gif 作为新的皮肤
            self.normal_image = Image.open("data1/angry.gif")
            self.load_images()  # 重新加载图像
            self.normal_index = 0
            self.img_label.config(image=self.normal_frames[self.normal_index])

            # 显示情绪框，显示为 'angry' 情绪
            self.emotion_label.config(image=self.emotion_images["angry"])
            self.emotion_label.place(x=75, y=50)  # 表情框位置

        elif emotion == "bored":
            # 加载并显示 bored.gif 作为新的皮肤
            self.normal_image = Image.open("data1/bored.gif")
            self.load_images()  # 重新加载图像
            self.normal_index = 0
            self.img_label.config(image=self.normal_frames[self.normal_index])

            # 显示情绪框，显示为 'bored' 情绪
            self.emotion_label.config(image=self.emotion_images["bored"])
            self.emotion_label.place(x=75, y=50)  # 表情框位置

        # 3秒后恢复原始皮肤
        self.master.after(3000, self.restore_default_skin)

        # 2秒后隐藏情绪框
        self.master.after(2000, lambda: self.emotion_label.place_forget())

    def restore_default_skin(self):
        """恢复最原始皮肤"""
        self.normal_image = self.default_image  # 恢复到原皮肤
        self.load_images()  # 重新加载原皮肤
        self.normal_index = 0
        self.img_label.config(image=self.normal_frames[self.normal_index])

    def set_touch_reaction(self):
        """设置触摸反应"""
        self.master.config(cursor="hand2")  # 设置鼠标为手形光标
        self.touch_timer = self.master.after(30000, self.reset_cursor)

    def reset_cursor(self):
        """重置鼠标光标为默认状态"""
        self.master.config(cursor=self.original_cursor)

    def switch_skin(self):
        """切换皮肤并重新加载 GIF 动画"""
        self.is_alternate_skin = not self.is_alternate_skin
        self.load_images()
        self.normal_index = 0

    def zoom_in(self, event=None):
        """放大显示"""
        self.scale_factor += 0.2
        self.load_images()
        self.normal_index = 0
        self.img_label.config(image=self.normal_frames[self.normal_index])

    def zoom_out(self, event=None):
        """缩小显示"""
        if self.scale_factor > 0.4:
            self.scale_factor -= 0.2
            self.load_images()
            self.normal_index = 0
            self.img_label.config(image=self.normal_frames[self.normal_index])


root = tk.Tk()
pet = DesktopPet(root)
root.mainloop()