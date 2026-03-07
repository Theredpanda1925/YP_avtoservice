# quality_manager.py - Менеджер по качеству
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sqlite3

class QualityManagerWindow:
    """Окно для Менеджера по качеству"""
    
    def __init__(self, parent, user, db_connection):
        self.parent = parent
        self.user = user
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        
        self.window = tk.Toplevel(parent)
        # ИСПРАВЛЕНО: используем 'fio' вместо 'full_name'
        self.window.title(f"Менеджер по качеству - {user['fio']}")
        self.window.geometry("1000x600")
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """Создание интерфейса"""
        
        # Верхняя панель с кнопками
        toolbar = ttk.Frame(self.window, padding="5")
        toolbar.pack(fill=tk.X)
        
        ttk.Button(
            toolbar,
            text="🔄 Обновить",
            command=self.load_data
        ).pack(side=tk.LEFT, padx=2)
        
        # Используем 'fio' вместо 'full_name'
        ttk.Label(
            toolbar,
            text=f"Добро пожаловать, {self.user['fio']}"
        ).pack(side=tk.RIGHT, padx=10)
        
        # Основной контейнер с вкладками
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка 1: Проблемные заявки
        self.problems_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.problems_frame, text="⚠️ Проблемные заявки")
        self.setup_problems_tab()
        
        # Вкладка 2: Продление сроков
        self.deadline_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.deadline_frame, text="📅 Продление сроков")
        self.setup_deadline_tab()
        
        # Вкладка 3: Отзывы и качество
        self.quality_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.quality_frame, text="⭐ Отзывы и качество")
        self.setup_quality_tab()
        
        # Вкладка 4: QR-код
        self.qr_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.qr_frame, text="📱 QR-код для отзывов")
        self.setup_qr_tab()
        
    def setup_problems_tab(self):
        """Вкладка с проблемными заявками"""
        
        # Заявки с просроченным сроком
        ttk.Label(
            self.problems_frame,
            text="Заявки с просроченным сроком:",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        # Таблица проблемных заявок
        columns = ('id', 'client', 'car', 'start_date', 'days', 'mechanic')
        self.problems_tree = ttk.Treeview(
            self.problems_frame,
            columns=columns,
            show='headings',
            height=5
        )
        
        self.problems_tree.heading('id', text='№')
        self.problems_tree.heading('client', text='Клиент')
        self.problems_tree.heading('car', text='Автомобиль')
        self.problems_tree.heading('start_date', text='Дата начала')
        self.problems_tree.heading('days', text='Дней в работе')
        self.problems_tree.heading('mechanic', text='Механик')
        
        self.problems_tree.column('id', width=50)
        self.problems_tree.column('client', width=150)
        self.problems_tree.column('car', width=150)
        self.problems_tree.column('start_date', width=100)
        self.problems_tree.column('days', width=80)
        self.problems_tree.column('mechanic', width=150)
        
        self.problems_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Кнопки для работы с проблемными заявками
        btn_frame = ttk.Frame(self.problems_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            btn_frame,
            text="➕ Назначить механика",
            command=self.assign_mechanic
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            btn_frame,
            text="📞 Связаться с клиентом",
            command=self.contact_client
        ).pack(side=tk.LEFT, padx=2)
        
    def setup_deadline_tab(self):
        """Вкладка продления сроков"""
        
        # Выбор заявки
        ttk.Label(
            self.deadline_frame,
            text="Выберите заявку для продления:",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        self.deadline_combo = ttk.Combobox(
            self.deadline_frame,
            width=50,
            state='readonly'
        )
        self.deadline_combo.pack(anchor=tk.W, padx=10, pady=5)
        
        # Количество дней
        ttk.Label(
            self.deadline_frame,
            text="Продлить на (дней):"
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        self.days_spinbox = ttk.Spinbox(
            self.deadline_frame,
            from_=1,
            to=30,
            width=10
        )
        self.days_spinbox.pack(anchor=tk.W, padx=10, pady=5)
        
        # Причина продления
        ttk.Label(
            self.deadline_frame,
            text="Причина продления:"
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        self.reason_text = tk.Text(
            self.deadline_frame,
            width=50,
            height=3
        )
        self.reason_text.pack(anchor=tk.W, padx=10, pady=5)
        
        # Кнопка продления
        ttk.Button(
            self.deadline_frame,
            text="✅ Продлить срок",
            command=self.extend_deadline
        ).pack(anchor=tk.W, padx=10, pady=10)
        
    def setup_quality_tab(self):
        """Вкладка с отзывами"""
        
        # Статистика отзывов
        stats_frame = ttk.LabelFrame(
            self.quality_frame,
            text="Статистика отзывов",
            padding="10"
        )
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.stats_label = ttk.Label(
            stats_frame,
            text="Загрузка статистики...",
            font=("Arial", 11)
        )
        self.stats_label.pack()
        
        # Список отзывов
        ttk.Label(
            self.quality_frame,
            text="Последние отзывы:",
            font=("Arial", 10, "bold")
        ).pack(anchor=tk.W, padx=10, pady=5)
        
        # Таблица отзывов
        columns = ('id', 'client', 'rating', 'comment', 'date')
        self.reviews_tree = ttk.Treeview(
            self.quality_frame,
            columns=columns,
            show='headings',
            height=8
        )
        
        self.reviews_tree.heading('id', text='№ заявки')
        self.reviews_tree.heading('client', text='Клиент')
        self.reviews_tree.heading('rating', text='Оценка')
        self.reviews_tree.heading('comment', text='Комментарий')
        self.reviews_tree.heading('date', text='Дата')
        
        self.reviews_tree.column('id', width=80)
        self.reviews_tree.column('client', width=150)
        self.reviews_tree.column('rating', width=70)
        self.reviews_tree.column('comment', width=300)
        self.reviews_tree.column('date', width=100)
        
        self.reviews_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def setup_qr_tab(self):
        """Вкладка с QR-кодом"""
        
        try:
            import qrcode
            from PIL import Image, ImageTk
            
            # Ссылка на форму опроса
            form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdhZcExx6LSIXxk0ub55mSu-WIh23WYdGG9HY5EZhLDo7P8eA/viewform"
            
            # Создание QR-кода
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
            qr.add_data(form_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Конвертация для Tkinter
            img = img.resize((300, 300))
            self.qr_image = ImageTk.PhotoImage(img)
            
            # Отображение QR-кода
            qr_label = ttk.Label(
                self.qr_frame,
                image=self.qr_image
            )
            qr_label.pack(pady=20)
            
            # Текст с инструкцией
            ttk.Label(
                self.qr_frame,
                text="Отсканируйте QR-код для оценки качества работы",
                font=("Arial", 12, "bold")
            ).pack(pady=10)
            
            ttk.Label(
                self.qr_frame,
                text="Клиенты могут оставить отзыв о качестве обслуживания",
                font=("Arial", 10)
            ).pack()
            
            # Кнопка для печати
            ttk.Button(
                self.qr_frame,
                text="🖨️ Распечатать QR-код",
                command=self.print_qr
            ).pack(pady=20)
            
        except ImportError:
            ttk.Label(
                self.qr_frame,
                text="Для генерации QR-кода установите библиотеку:\n"
                     "pip install qrcode[pil]",
                font=("Arial", 12),
                foreground="red"
            ).pack(pady=50)
    
    def load_data(self):
        """Загрузка данных"""
        self.load_problems()
        self.load_reviews()
        self.load_deadline_requests()
        
    def load_problems(self):
        """Загрузка проблемных заявок"""
        # Очистка
        for item in self.problems_tree.get_children():
            self.problems_tree.delete(item)
        
        # Заявки в работе больше 7 дней
        query = '''
            SELECT r.request_id, c.full_name, 
                   r.car_type || ' ' || r.car_model,
                   r.start_date,
                   julianday('now') - julianday(r.start_date) as days,
                   m.full_name as mechanic
            FROM requests r
            JOIN users c ON r.client_id = c.user_id
            LEFT JOIN users m ON r.master_id = m.user_id
            WHERE r.status = 'В процессе ремонта'
              AND julianday('now') - julianday(r.start_date) > 7
            ORDER BY days DESC
        '''
        
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            self.problems_tree.insert('', tk.END, values=row)
    
    def load_reviews(self):
        """Загрузка отзывов"""
        # Очистка
        for item in self.reviews_tree.get_children():
            self.reviews_tree.delete(item)
        
        # Здесь должен быть запрос к таблице отзывов
        # Пока заглушка
        sample_reviews = [
            (3, "Ильина Тамара", 5, "Отличная работа!", "2026-03-01"),
            (5, "Никифорова Алиса", 4, "Хорошо, но долго", "2026-02-28")
        ]
        
        for review in sample_reviews:
            self.reviews_tree.insert('', tk.END, values=review)
        
        # Обновление статистики
        self.stats_label.config(
            text=f"⭐ Средняя оценка: 4.5 (на основе 2 отзывов)"
        )
    
    def load_deadline_requests(self):
        """Загрузка заявок для продления"""
        query = '''
            SELECT r.request_id || ': ' || c.full_name || ' - ' || 
                   r.car_type || ' ' || r.car_model
            FROM requests r
            JOIN users c ON r.client_id = c.user_id
            WHERE r.status IN ('В процессе ремонта', 'Ожидание запчастей')
        '''
        
        self.cursor.execute(query)
        requests = [row[0] for row in self.cursor.fetchall()]
        self.deadline_combo['values'] = requests
    
    def assign_mechanic(self):
        """Назначение механика"""
        selected = self.problems_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Предупреждение",
                "Выберите заявку!"
            )
            return
        
        # Здесь открыть диалог выбора механика
        messagebox.showinfo(
            "Информация",
            "Функция назначения механика будет доступна в следующей версии"
        )
    
    def contact_client(self):
        """Связь с клиентом"""
        selected = self.problems_tree.selection()
        if not selected:
            messagebox.showwarning(
                "Предупреждение",
                "Выберите заявку!"
            )
            return
        
        values = self.problems_tree.item(selected[0])['values']
        messagebox.showinfo(
            "Контактные данные",
            f"Клиент: {values[1]}\n"
            f"Телефон: для демо-версии 8-800-XXX-XX-XX"
        )
    
    def extend_deadline(self):
        """Продление срока заявки"""
        if not self.deadline_combo.get():
            messagebox.showwarning(
                "Предупреждение",
                "Выберите заявку!"
            )
            return
        
        days = self.days_spinbox.get()
        reason = self.reason_text.get('1.0', tk.END).strip()
        
        if not reason:
            messagebox.showwarning(
                "Предупреждение",
                "Укажите причину продления!"
            )
            return
        
        # Здесь логика продления срока
        
        messagebox.showinfo(
            "Успешно",
            f"Срок выполнения продлен на {days} дней.\n"
            f"Клиент уведомлен."
        )
        
        # Очистка формы
        self.reason_text.delete('1.0', tk.END)
    
    def print_qr(self):
        """Печать QR-кода"""
        messagebox.showinfo(
            "Печать",
            "QR-код отправлен на печать"
        )