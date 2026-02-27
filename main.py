# main.py - Точка входа в приложение
import tkinter as tk
from auth import AuthWindow

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthWindow(root)
    root.mainloop()