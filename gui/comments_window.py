# gui/comments_window.py - Окно комментариев
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class CommentsWindow:
    def __init__(self, parent, request, comments, current_user, users):
        self.request = request
        self.comments = comments
        self.current_user = current_user
        self.users = users
        
        # Создание окна
        self.window = tk.Toplevel(parent)
        self.window.title(f"Комментарии к заявке №{request['id']}")
        self.window.geometry("600x500")
        self.window.transient(parent)
        self.window.grab_set()
        
        # Центрирование окна
        self.center_window()
        
        # Создание виджетов
        self.create_widgets()
        
        # Загрузка комментариев
        self.load_comments()
        
    def center_window(self):
        """Центрирует окно"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = self.window.winfo_screenwidth() // 2 - width // 2
        y = self.window.winfo_screenheight() // 2 - height // 2
        self.window.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Создает элементы интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Информация о заявке
        info_frame = ttk.LabelFrame(main_frame, text="Информация о заявке", padding="5")
        info_frame.pack(fill=tk.X, pady=5)
        
        client_name = "Неизвестно"
        for user in self.users:
            if user['id'] == self.request['client_id']:
                client_name = user['fio']
                break
        
        ttk.Label(
            info_frame,
            text=f"Клиент: {client_name} | Авто: {self.request['car_type']} {self.request['car_model']} | Статус: {self.request['status']}"
        ).pack(anchor=tk.W)
        
        # Фрейм для списка комментариев
        comments_frame = ttk.LabelFrame(main_frame, text="История комментариев", padding="5")
        comments_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Создание текстового поля с прокруткой
        scrollbar = ttk.Scrollbar(comments_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.comments_text = tk.Text(
            comments_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED,
            height=15
        )
        self.comments_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.comments_text.yview)
        
        # Фрейм для нового комментария
        new_comment_frame = ttk.LabelFrame(main_frame, text="Новый комментарий", padding="5")
        new_comment_frame.pack(fill=tk.X, pady=5)
        
        self.comment_entry = tk.Text(new_comment_frame, height=3, width=60)
        self.comment_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        # Кнопка отправки
        send_btn = ttk.Button(
            new_comment_frame,
            text="Отправить",
            command=self.add_comment,
            width=15
        )
        send_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Кнопка закрытия
        close_btn = ttk.Button(
            main_frame,
            text="Закрыть",
            command=self.window.destroy,
            width=15
        )
        close_btn.pack(pady=10)
        
    def load_comments(self):
        """Загружает и отображает комментарии"""
        self.comments_text.config(state=tk.NORMAL)
        self.comments_text.delete('1.0', tk.END)
        
        # Фильтрация комментариев для данной заявки
        request_comments = [c for c in self.comments if c['request_id'] == self.request['id']]
        
        if not request_comments:
            self.comments_text.insert(tk.END, "Нет комментариев.\n")
        else:
            for comment in request_comments:
                # Поиск автора
                author = "Неизвестно"
                for user in self.users:
                    if user['id'] == comment['master_id']:
                        author = user['fio']
                        break
                
                # Добавление комментария
                self.comments_text.insert(tk.END, f"[{author}]\n")
                self.comments_text.insert(tk.END, f"{comment['message']}\n")
                self.comments_text.insert(tk.END, "-" * 50 + "\n")
        
        self.comments_text.config(state=tk.DISABLED)
        
    def add_comment(self):
        """Добавляет новый комментарий"""
        comment_text = self.comment_entry.get('1.0', tk.END).strip()
        
        if not comment_text:
            messagebox.showwarning(
                "Предупреждение",
                "Введите текст комментария!"
            )
            return
        
        # Генерация нового ID
        new_id = max([c['id'] for c in self.comments]) + 1 if self.comments else 1
        
        # Создание нового комментария
        new_comment = {
            'id': new_id,
            'message': comment_text,
            'master_id': self.current_user['id'],
            'request_id': self.request['id']
        }
        
        # Добавление в список
        self.comments.append(new_comment)
        
        # Очистка поля ввода
        self.comment_entry.delete('1.0', tk.END)
        
        # Обновление отображения
        self.load_comments()
        
        messagebox.showinfo(
            "Успешно",
            "Комментарий добавлен!"
        )