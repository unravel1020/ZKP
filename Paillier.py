import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
import random
import paillier.keygen as keygen
import paillier.crypto as crypto

# Alice生成自己的公私钥(足够长)
pk, sk = keygen.generate_keys()


def compare_wealth():
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        result = compare(a, b)
        messagebox.showinfo("比较结果", result)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的整数")
    except Exception as e:
        messagebox.showerror("错误", str(e))


# 比较Alice的财富a和Bob的财富b
def compare(a, b):
    # Bob生成两个随机数x和y
    x = random.getrandbits(100)
    y = random.getrandbits(128)

    # Alice公布自己公钥pk
    print("Alice: pk =", pk)

    # Alice计算a的密文并公布
    e_a = crypto.encrypt(pk, a)
    print("Alice: E(a) =", e_a)

    # Bob计算b*x+y的密文并公布
    n, _ = pk
    e_bxy = crypto.encrypt(pk, b * x + y)
    print("Bob: E(b*x+y) =", e_bxy)

    # Bob计算a*x+y的密文并公布
    e_axy = crypto.secure_addition(
        crypto.scalar_multiplication(e_a, x, n),
        crypto.encrypt(pk, y),
        n,
    )
    print("Bob: E(a*x+y) =", e_axy)

    # Alice根据密文反解出b*x+y
    bxy = crypto.decrypt(pk, sk, e_bxy)

    # Alice根据密文反解出a*x+y
    axy = crypto.decrypt(pk, sk, e_axy)

    # Alice公布最终的大小结果
    if axy > bxy:
        return "Alice is greater than Bob"
    elif bxy > axy:
        return "Bob is greater than Alice"
    else:
        return "tie"


if __name__ == '__main__':
    # 初始化GUI
    root = tk.Tk()
    root.title("财富比较工具")

    # 设置窗口大小和位置
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.4)
    window_height = int(screen_height * 0.4)
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 输入框
    label_a = tk.Label(root, text="Alice的财富(请输入整数）:")
    label_a.pack(pady=(20, 0))
    entry_a = tk.Entry(root)
    entry_a.pack(pady=(0, 20))

    label_b = tk.Label(root, text="Bob的财富（请输入整数）:")
    label_b.pack(pady=(20, 0))
    entry_b = tk.Entry(root)
    entry_b.pack(pady=(0, 40))

    # 按钮
    compare_button = tk.Button(root, text="比较", command=compare_wealth)
    compare_button.pack()

    # 运行GUI
    root.mainloop()
