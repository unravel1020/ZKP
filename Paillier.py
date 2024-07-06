import tkinter as tk
from tkinter import messagebox
import random
import paillier.keygen as keygen
import paillier.crypto as crypto

# 生成RSA公私钥对
pk, sk = keygen.generate_keys()


def encrypt_value(value):
    """
    使用Paillier加密算法加密值。
    """
    return crypto.encrypt(pk, value)


def calculate_secure_addition(encrypted_a, multiplier, random_value):
    """
    计算安全的加法：E(a * x + y)，其中 a 是加密的，x 和 y 是随机值。
    """
    n, _ = pk
    encrypted_x_a = crypto.scalar_multiplication(encrypted_a, multiplier, n)
    encrypted_y = crypto.encrypt(pk, random_value)
    return crypto.secure_addition(encrypted_x_a, encrypted_y, n)


def compare_wealth(a, b):
    """
    比较Alice的财富a和Bob的财富b。
    返回比较结果。
    """
    try:
        x = random.getrandbits(100)
        y = random.getrandbits(128)

        # Alice计算a的密文并公布
        e_a = encrypt_value(a)

        # Bob计算b*x+y的密文并公布
        e_bxy = encrypt_value(b * x + y)

        # Bob计算a*x+y的密文并公布
        e_axy = calculate_secure_addition(e_a, x, y)

        # Alice解密得到b*x+y和a*x+y
        bxy = crypto.decrypt(pk, sk, e_bxy)
        axy = crypto.decrypt(pk, sk, e_axy)

        # 比较解密后的结果
        if axy > bxy:
            return "Alice is wealthier than Bob"
        elif bxy > axy:
            return "Bob is wealthier than Alice"
        else:
            return "Alice and Bob have equal wealth"
    except Exception as e:
        return f"An error occurred during comparison: {e}"


def create_ui():
    """
    创建GUI界面，用于输入Alice和Bob的财富并进行比较。
    """
    root = tk.Tk()
    root.title("Wealth Comparison")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.4)
    window_height = int(screen_height * 0.4)
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    tk.Label(root, text="Alice's Wealth (Enter an integer):").pack(pady=(20, 0))
    entry_a = tk.Entry(root)
    entry_a.pack(pady=(0, 20))

    tk.Label(root, text="Bob's Wealth (Enter an integer):").pack(pady=(20, 0))
    entry_b = tk.Entry(root)
    entry_b.pack(pady=(0, 40))

    def on_compare():
        try:
            a = int(entry_a.get())
            b = int(entry_b.get())
            result = compare_wealth(a, b)
            messagebox.showinfo("Comparison Result", result)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers")

    tk.Button(root, text="Compare", command=on_compare).pack()

    return root


if __name__ == '__main__':
    app = create_ui()
    app.mainloop()
