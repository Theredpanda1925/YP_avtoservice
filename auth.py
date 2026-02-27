# auth.py - Модуль авторизации
import tkinter as tk
from tkinter import messagebox, ttk
import os  # ВАЖНО: добавить этот импорт
from data_manager import DataManager
from gui.main_window import MainWindow

class AuthWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Авторизация - АвтоТранс")
        self.root.geometry("350x270")
        self.root.resizable(False, False)
        
        # Центрирование окна
        self.center_window()
        
        # Загрузка данных из существующих файлов
        self.data_manager = DataManager()
        
        # Пути к файлам (в текущей папке)
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        self.users = self.data_manager.load_users(os.path.join(base_path, "inputDataUsers.txt"))
        self.requests = self.data_manager.load_requests(os.path.join(base_path, "inputDataRequests.txt"))
        self.comments = self.data_manager.load_comments(os.path.join(base_path, "inputDataComments.txt"))
        
        # Преобразуем логины в понятный вид для демо
        self.prepare_users_for_demo()
        
        # Проверка загрузки данных
        print(f"Загружено пользователей: {len(self.users)}")
        print(f"Загружено заявок: {len(self.requests)}")
        print(f"Загружено комментариев: {len(self.comments)}")
        
        # Создание виджетов
        self.create_widgets()
        
    def prepare_users_for_demo(self):
        """Преобразует логины в понятный вид для демонстрации"""
        # Соответствие ID пользователей новым логинам
        demo_credentials = {
            1: {'login': 'manager', 'password': '123'},      # Белов - Менеджер
            2: {'login': 'mechanic1', 'password': '123'},    # Харитонова - Автомеханик
            3: {'login': 'mechanic2', 'password': '123'},    # Марков - Автомеханик
            4: {'login': 'operator1', 'password': '123'},    # Громова - Оператор
            5: {'login': 'operator2', 'password': '123'},    # Карташова - Оператор
            6: {'login': 'client1', 'password': '123'},      # Касаткин - Заказчик
            7: {'login': 'client2', 'password': '123'},      # Ильина - Заказчик
            8: {'login': 'client3', 'password': '123'},      # Елисеева - Заказчик
            9: {'login': 'client4', 'password': '123'},      # Никифорова - Заказчик
            10: {'login': 'mechanic3', 'password': '123'}    # Васильев - Автомеханик
        }
        
        for user in self.users:
            user_id = user['id']
            if user_id in demo_credentials:
                user['login'] = demo_credentials[user_id]['login']
                user['password'] = demo_credentials[user_id]['password']
        
        print("\n=== ТЕСТОВЫЕ УЧЁТНЫЕ ДАННЫЕ ===")
        print("manager / 123 - Менеджер")
        print("mechanic1 / 123 - Автомеханик (Харитонова)")
        print("mechanic2 / 123 - Автомеханик (Марков)")
        print("mechanic3 / 123 - Автомеханик (Васильев)")
        print("operator1 / 123 - Оператор (Громова)")
        print("operator2 / 123 - Оператор (Карташова)")
        print("client1 / 123 - Заказчик")
        print("client2 / 123 - Заказчик")
        print("client3 / 123 - Заказчик")
        print("client4 / 123 - Заказчик")
        print("================================\n")
        
    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Создает элементы интерфейса"""
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="Вход в систему учёта заявок", 
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=10)
        
        # Фрейм для формы входа
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Логин
        ttk.Label(frame, text="Логин:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.login_entry = ttk.Entry(frame, width=20)
        self.login_entry.grid(row=0, column=1, pady=5)
        self.login_entry.focus()
        
        # Пароль
        ttk.Label(frame, text="Пароль:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(frame, width=20, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)
        
        # Привязка клавиши Enter
        self.password_entry.bind('<Return>', lambda event: self.login())
        
        # Кнопка входа
        login_btn = ttk.Button(
            frame, 
            text="Войти", 
            command=self.login,
            width=15
        )
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Подсказка с тестовыми данными
        hint_text = "Тестовые аккаунты:\n"
        hint_text += "manager/123 (менеджер)\n"
        hint_text += "mechanic1/123 (механик)\n"
        hint_text += "operator1/123 (оператор)\n"
        hint_text += "client1/123 (заказчик)"
        
        hint_label = tk.Label(
            frame,
            text=hint_text,
            font=("Arial", 8),
            fg="gray",
            justify=tk.LEFT
        )
        hint_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Кнопка выхода
        exit_btn = ttk.Button(
            frame,
            text="Выход",
            command=self.root.quit,
            width=15
        )
        exit_btn.grid(row=4, column=0, columnspan=2, pady=5)
        
    def login(self):
        """Проверяет логин и пароль"""
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not login or not password:
            messagebox.showwarning(
                "Предупреждение",
                "Введите логин и пароль!"
            )
            return
        
        # Поиск пользователя
        current_user = None
        for user in self.users:
            if user['login'].lower() == login.lower() and user['password'] == password:
                current_user = user
                break
        
        if current_user:
            messagebox.showinfo(
                "Успешно",
                f"Добро пожаловать, {current_user['fio']}!\n"
                f"Ваша роль: {current_user['role']}"
            )
            # Открываем главное окно
            self.root.withdraw()  # Скрываем окно авторизации
            main_window = tk.Toplevel()
            app = MainWindow(
                main_window, 
                current_user, 
                self.requests, 
                self.comments,
                self.users
            )
            
            # Когда главное окно закрывается, показываем окно авторизации
            main_window.protocol("WM_DELETE_WINDOW", lambda: self.on_main_window_close(main_window))
        else:
            messagebox.showerror(
                "Ошибка авторизации",
                "Неверный логин или пароль!\n"
                "Используйте тестовые данные:\n"
                "manager / 123\n"
                "mechanic1 / 123\n"
                "operator1 / 123\n"
                "client1 / 123"
            )
            self.password_entry.delete(0, tk.END)
            self.login_entry.focus()
    
    def on_main_window_close(self, main_window):
        """Обработчик закрытия главного окна"""
        main_window.destroy()
        self.root.deiconify()  # Показываем окно авторизации