import tkinter as tk
import random

# 定义不同的皮肤（用简单的文本表示）
skins = ["(=^_^=)", "(=^o^=)", "(=^_^#)", "(=^_^*)"]

# 定义简单的表情响应
responses = {
    "你好": "(=^_^=) 你好！",
    "开心": "(=^o^=) 我也很开心！",
    "生气": "(=^_^#) 别生气嘛~",
    "害羞": "(=^_^*) 不要害羞哦~"
}

def get_random_skin():
    return random.choice(skins)

def get_response(user_input):
    return responses.get(user_input, "(=^_^=) 我不太明白你的意思~")

def update_pet_expression():
    user_input = entry.get()
    response = get_response(user_input)
    pet_label.config(text=response)

def main():
    # 创建主窗口
    root = tk.Tk()
    root.title("桌面宠物")

    # 随机选择一个皮肤
    current_skin = get_random_skin()

    # 显示当前皮肤
    global pet_label
    pet_label = tk.Label(root, text=current_skin, font=("Arial", 40))
    pet_label.pack(pady=20)

    # 创建输入框
    global entry
    entry = tk.Entry(root, font=("Arial", 20))
    entry.pack(pady=10)

    # 创建按钮
    button = tk.Button(root, text="对话", command=update_pet_expression, font=("Arial", 20))
    button.pack(pady=10)

    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()