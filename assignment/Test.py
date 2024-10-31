import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDesktopWidget


class DesktopPet(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口为无边框并始终置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)

        # 设置窗口透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # 初始化宠物的标签
        self.label = QLabel(self)

        # 加载并缩放图片
        pixmap = QPixmap(r"D:\Term1\SD5913\Assignment\pfad\pet.png")
        if pixmap.isNull():
            print("图片加载失败，请检查路径")
        else:
            # 缩放图片到150x150大小并保持比例
            pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(pixmap)
            self.label.setScaledContents(True)  # 自动缩放内容
            self.label.resize(pixmap.size())  # 调整标签大小以适应图片
            self.resize(pixmap.size())  # 调整窗口大小以适应图片

        # 将窗口移动到屏幕中心
        self.center()

        # 宠物的移动开关
        #self.moving = False
        #self.offset = None

        # 添加自动移动功能
        #self.timer = QTimer(self)
        #self.timer.timeout.connect(self.random_move)
        #self.timer.start(2000)  # 每2秒移动一次

    def center(self):
        """将窗口移动到屏幕中央"""
        screen_geometry = QDesktopWidget().availableGeometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.moving = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.moving:
            self.move(event.globalPos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.moving = False

    def random_move(self):
        screen_geometry = QApplication.desktop().availableGeometry(self)
        x = self.x() + 20
        y = self.y() + 20
        if x > screen_geometry.width() - self.width():
            x = 0
        if y > screen_geometry.height() - self.height():
            y = 0
        self.move(x, y)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = DesktopPet()

    if pet:
        pet.show()
    else:
        print("窗口对象创建失败")

    sys.exit(app.exec_())
