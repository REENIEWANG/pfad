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
        self.buttons = []  # 用来保存所有按钮的 Canvas 对象
        try:
            # 加载初始皮肤 GIF 和备用皮肤 GIF
            self.normal_image = Image.open("Image Resources/normal.gif")
            self.default_image = Image.open("Image Resources/normal.gif")  # 默认皮肤
            self.alternate_image = Image.open("Image Resources/normal2.gif")
            self.icon_images = [
                Image.open("Image Resources/uialarm.png"),
                Image.open("Image Resources/uitouch.png"),
                Image.open("Image Resources/uichat.png"),
                Image.open("Image Resources/uizoom.png"),
                Image.open("Image Resources/uiskin.png"),
                Image.open("Image Resources/uiexist.png")
            ]
            # 加载手形光标图像
            self.hand_cursor_image = Image.open("Image Resources/hand.png")
            self.hand_cursor = ImageTk.PhotoImage(self.hand_cursor_image.resize((30, 30)))

            # 加载表情框图片
            self.emotion_images = {
                "happy": ImageTk.PhotoImage(Image.open("Image Resources/uikuang_happy.png")),
                "sad": ImageTk.PhotoImage(Image.open("Image Resources/uikuang_sad.png")),
                "angry": ImageTk.PhotoImage(Image.open("Image Resources/uikuang_angry.png")),
                "bored": ImageTk.PhotoImage(Image.open("Image Resources/uikuang_bored.png"))
            }

            # 加载闹钟图像（假设为一张图片）
            self.alarm_image = Image.open("Image Resources/alarmgif.gif")  # 这里假设是一个GIF文件
        except Exception as e:
            print(f"加载图像时发生错误: {e}")
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
        self.img_label.bind("<B1-Motion>",self.do_drag)


        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 初始化情绪显示
        self.emotion_label = tk.Label(master, bg="gray")
        self.emotion_label.place_forget()  # 初始隐藏

        # 初始化倒计时标签
        self.countdown_label = tk.Label(master, font=("Arial", 16), bg="gray", fg="red")
        self.countdown_label.place_forget()  # 初始隐藏

        # 初始化倒计时剩余时间（设置初值为 0）
        self.remaining_seconds = 0

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

        # Ensure original_image is always set as a Tkinter-compatible PhotoImage
        self.original_image = self.normal_frames[0] if self.normal_frames else None

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
            self.show_alarm()  # 显示闹钟并启动倒计时
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
            print("功能5：更换皮肤")
            self.toggle_skin()  # 调用 toggle_skin 方法来更换皮肤
        elif idx == 5:
            print("功能6：退出")
            self.exit_animation()  # 执行退出动画后退出程序

    def exit_animation(self):
        """显示退出动画并延迟退出程序"""
        # 切换皮肤到退出动画
        self.normal_image = Image.open("Image Resources/exit.gif")
        self.load_images()  # 重新加载退出图像
        self.normal_index = 0
        self.img_label.config(image=self.normal_frames[self.normal_index])  # 设置为退出动画图像

        # 延迟 2 秒后退出程序
        self.master.after(2000, self.on_closing)

        # 定义 toggle_skin 方法
    def toggle_skin(self):
        """切换皮肤并重新加载 GIF 动画"""
        self.is_alternate_skin = not self.is_alternate_skin  # 切换皮肤标志
        self.load_images()  # 重新加载图像
        self.normal_index = 0  # 从第一帧开始显示

    def show_alarm(self):
        """显示闹钟动画和倒计时"""
        # 切换皮肤到闹钟皮肤
        self.normal_image = Image.open("Image Resources/alarmgif.gif")
        self.load_images()  # 重新加载图像
        self.normal_index = 0
        self.img_label.config(image=self.normal_frames[self.normal_index])  # 设置为闹钟图像

        # 显示倒计时标签
        self.countdown_label.place(x=100, y=50)  # 设置位置
        self.start_countdown(5)  # 设置倒计时为5分钟

    def start_countdown(self, remaining_seconds):
        """启动倒计时"""
        self.remaining_seconds = remaining_seconds  # 将剩余时间存储在类的属性中

        def update_timer():
            minutes, seconds = divmod(self.remaining_seconds, 60)
            self.countdown_label.config(text=f"{minutes:02}:{seconds:02}")
            if self.remaining_seconds > 0:
                self.remaining_seconds -= 1
                self.master.after(1000, update_timer)
            else:
                self.hide_alarm()  # 倒计时结束后隐藏闹钟
                self.restore_default_skin()  # 恢复默认皮肤

        update_timer()

    def hide_alarm(self):
        """恢复原皮肤并隐藏倒计时标签"""
        self.countdown_label.place_forget()  # 隐藏倒计时标签
        self.img_label.config(image=self.original_image)  # 恢复原始皮肤

    def show_emotion_options(self):
        """显示聊天选项（开心，伤心，生气，无聊）"""
        options = ["happy", "sad", "angry", "bored"]
        button_width = 60  # 按钮宽度
        button_height = 30  # 按钮高度
        spacing = 15  # 每个按钮之间的间距
        max_buttons_per_row = 4  # 一行最多显示 4 个按钮

        for i, emotion in enumerate(options):
            # 计算按钮的行列位置
            row = i // max_buttons_per_row  # 计算行数
            col = i % max_buttons_per_row  # 计算列数

            # 计算按钮的 x 和 y 坐标
            x = 10 + col * (button_width + spacing)  # 按列分布
            y = 10 + row * (button_height + spacing)  # 按行分布，给每行增加一些垂直间距

            # 创建圆角按钮
            self.create_rounded_button(x, y, button_width, button_height, emotion)

    def create_rounded_button(self, x, y, width, height, text):
        canvas = tk.Canvas(self.master, width=width, height=height, bd=0, highlightthickness=0)
        canvas.place(x=x, y=y)
        radius = 10
        canvas.create_oval(0, 0, radius * 2, radius * 2, fill="white", outline="white")  # 左上角
        canvas.create_oval(width - radius * 2, 0, width, radius * 2, fill="white", outline="white")  # 右上角
        canvas.create_oval(0, height - radius * 2, radius * 2, height, fill="white", outline="white")  # 左下角
        canvas.create_oval(width - radius * 2, height - radius * 2, width, height, fill="white", outline="white")  # 右下角
        canvas.create_rectangle(radius, 0, width - radius, height, fill="white", outline="white")
        canvas.create_rectangle(0, radius, width, height - radius, fill="white", outline="white")
        canvas.create_text(width / 2, height / 2, text=text.capitalize(), font=("Arial", 10), fill="black")

        # 为按钮绑定点击事件
        canvas.tag_bind("button", "<Button-1>", lambda event, e=text: self.show_emotion(e))

        # 将按钮的 Canvas 对象加入列表
        self.buttons.append(canvas)

        canvas.tag_bind("button", "<Leave>", lambda event: self.remove_buttons_after_delay())

        canvas.create_rectangle(0, 0, width, height, outline="", fill="", tags="button")

    def remove_buttons_after_delay(self):
        """延迟 4 秒钟后移除所有按钮"""
        # 使用 after 方法延迟删除所有按钮
        self.master.after(4000, self.remove_all_buttons)

    def remove_all_buttons(self):
        """移除所有按钮"""
        for canvas in self.buttons:
            canvas.destroy()  # 销毁所有按钮
        self.buttons.clear()  # 清空按钮列表


    def show_emotion(self, emotion):
        """显示选中情绪的图像"""
        self.original_image = self.normal_image  # 保存当前皮肤（无论是否为原皮肤）

        if emotion == "happy":
            # 加载并显示 happy.gif 作为新的皮肤
            self.normal_image = Image.open("Image Resources/happy.gif")
            self.load_images()  # 重新加载图像
            self.normal_index = 0
            self.img_label.config(image=self.normal_frames[self.normal_index])

            # 显示情绪框，显示为 'happy' 情绪
            self.emotion_label.config(image=self.emotion_images["happy"])
            self.emotion_label.place(x=75, y=50)  # 表情框位置

        elif emotion == "sad":
            # 加载并显示 sad.gif 作为新的皮肤
            self.normal_image = Image.open("Image Resources/sad.gif")
            self.load_images()  # 重新加载图像
            self.normal_index = 0
            self.img_label.config(image=self.normal_frames[self.normal_index])

            # 显示情绪框，显示为 'sad' 情绪
            self.emotion_label.config(image=self.emotion_images["sad"])
            self.emotion_label.place(x=75, y=50)  # 表情框位置

        elif emotion == "angry":
            # 加载并显示 angry.gif 作为新的皮肤
            self.normal_image = Image.open("Image Resources/angry.gif")
            self.load_images()  # 重新加载图像
            self.normal_index = 0
            self.img_label.config(image=self.normal_frames[self.normal_index])

            # 显示情绪框，显示为 'angry' 情绪
            self.emotion_label.config(image=self.emotion_images["angry"])
            self.emotion_label.place(x=75, y=50)  # 表情框位置

        elif emotion == "bored":
            # 加载并显示 bored.gif 作为新的皮肤
            self.normal_image = Image.open("Image Resources/bored.gif")
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
        self.touch_active = True  # 激活触摸反应状态
        self.touch_timer = self.master.after(30000, self.reset_cursor)  # 30 秒后重置光标

        # 修改悬停事件逻辑，在触摸反应期间增加换 GIF 功能
        self.img_label.bind("<Enter>", self.on_touch_hover)
        self.img_label.bind("<Leave>", self.reset_touch_hover)

    def reset_cursor(self):
        """重置鼠标光标为默认状态"""
        self.master.config(cursor=self.original_cursor)
        self.touch_active = False  # 取消触摸反应状态

        # 恢复默认悬停事件逻辑
        self.img_label.bind("<Enter>", self.on_hover)
        self.img_label.bind("<Leave>", self.on_leave)

    def on_touch_hover(self, event):
        """触摸反应期间的悬停事件"""
        if self.touch_active:  # 仅在触摸反应激活时处理
            if self.hover_timer:
                self.master.after_cancel(self.hover_timer)
            self.hover_timer = self.master.after(2000, self.set_happy_gif)  # 2 秒后切换为 happy.gif

    def reset_touch_hover(self, event):
        """触摸反应期间的鼠标离开事件"""
        if self.hover_timer:
            self.master.after_cancel(self.hover_timer)
            self.hover_timer = None

    def set_happy_gif(self):
        """切换到 happy.gif 并设置定时恢复原皮肤"""
        if self.touch_active:  # 确保触发仅在触摸模式有效时
            self.show_emotion("happy")

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
