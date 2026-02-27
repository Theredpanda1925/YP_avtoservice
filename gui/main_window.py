# gui/main_window.py - Главное окно приложения
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from gui.request_dialog import RequestDialog
from gui.comments_window import CommentsWindow

class MainWindow:
    def __init__(self, root, current_user, requests, comments, users):
        self.root = root
        self.current_user = current_user
        self.requests = requests
        self.comments = comments
        self.users = users
        self.filtered_requests = requests.copy()
        
        # Настройка окна
        self.root.title(f"Автосервис 'АвтоТранс' - Учёт заявок ({current_user['role']}: {current_user['fio']})")
        self.root.geometry("1200x600")
        
        # Центрирование окна
        self.center_window()
        
        # Создание меню
        self.create_menu()
        
        # Создание панели инструментов
        self.create_toolbar()
        
        # Создание панели фильтрации
        self.create_filter_panel()
        
        # Создание таблицы заявок
        self.create_requests_table()
        
        # Создание статусной строки
        self.create_status_bar()
        
        # Заполнение таблицы
        self.refresh_table()
        
        # Обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_menu(self):
        """Создает главное меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Обновить", command=self.refresh_table)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_closing)
        
        # Меню Справка
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
        
    def create_toolbar(self):
        """Создает панель инструментов"""
        toolbar = ttk.Frame(self.root, padding="5")
        toolbar.pack(fill=tk.X)
        
        # Кнопки доступны в зависимости от роли
        if self.current_user['role'] in ['Менеджер', 'Оператор']:
            ttk.Button(
                toolbar,
                text="➕ Создать заявку",
                command=self.create_request,
                width=15
            ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="✏️ Редактировать",
            command=self.edit_request,
            width=12
        ).pack(side=tk.LEFT, padx=2)
        
        if self.current_user['role'] == 'Автомеханик':
            ttk.Button(
                toolbar,
                text="💬 Комментарии",
                command=self.open_comments,
                width=12
            ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="📊 Статистика",
            command=self.show_statistics,
            width=12
        ).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            toolbar,
            text="🚪 Выход",
            command=self.on_closing,
            width=8
        ).pack(side=tk.RIGHT, padx=2)
        
    def create_filter_panel(self):
        """Создает панель фильтрации и поиска"""
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация и поиск", padding="5")
        filter_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Фильтр по статусу
        ttk.Label(filter_frame, text="Статус:").grid(row=0, column=0, padx=5)
        self.status_filter = ttk.Combobox(
            filter_frame,
            values=["Все", "Новая заявка", "В процессе ремонта", "Готова к выдаче"],
            state="readonly",
            width=20
        )
        self.status_filter.set("Все")
        self.status_filter.grid(row=0, column=1, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Применить фильтр",
            command=self.apply_filter
        ).grid(row=0, column=2, padx=5)
        
        # Поиск
        ttk.Label(filter_frame, text="Поиск (ID или модель):").grid(row=0, column=3, padx=5)
        self.search_entry = ttk.Entry(filter_frame, width=25)
        self.search_entry.grid(row=0, column=4, padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_requests())
        
        ttk.Button(
            filter_frame,
            text="Найти",
            command=self.search_requests
        ).grid(row=0, column=5, padx=5)
        
        ttk.Button(
            filter_frame,
            text="Сбросить",
            command=self.reset_filter
        ).grid(row=0, column=6, padx=5)
        
    def create_requests_table(self):
        """Создает таблицу для отображения заявок"""
        # Фрейм для таблицы и скроллбаров
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создание скроллбаров
        v_scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)
        h_scrollbar = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        
        # Создание таблицы
        columns = ('id', 'date', 'client', 'car', 'status', 'master', 'description')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            height=15
        )
        
        # Настройка скроллбаров
        v_scrollbar.config(command=self.tree.yview)
        h_scrollbar.config(command=self.tree.xview)
        
        # Определение заголовков
        self.tree.heading('id', text='№', command=lambda: self.sort_column('id', False))
        self.tree.heading('date', text='Дата', command=lambda: self.sort_column('date', False))
        self.tree.heading('client', text='Клиент', command=lambda: self.sort_column('client', False))
        self.tree.heading('car', text='Автомобиль', command=lambda: self.sort_column('car', False))
        self.tree.heading('status', text='Статус', command=lambda: self.sort_column('status', False))
        self.tree.heading('master', text='Механик', command=lambda: self.sort_column('master', False))
        self.tree.heading('description', text='Описание', command=lambda: self.sort_column('description', False))
        
        # Настройка ширины колонок
        self.tree.column('id', width=50, minwidth=40)
        self.tree.column('date', width=90, minwidth=70)
        self.tree.column('client', width=150, minwidth=120)
        self.tree.column('car', width=150, minwidth=120)
        self.tree.column('status', width=130, minwidth=100)
        self.tree.column('master', width=150, minwidth=120)
        self.tree.column('description', width=300, minwidth=200)
        
        # Размещение элементов
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Настройка растягивания
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Привязка двойного клика
        self.tree.bind('<Double-1>', lambda e: self.edit_request())
        
    def create_status_bar(self):
        """Создает строку состояния"""
        self.status_bar = ttk.Label(
            self.root,
            text=f"Всего заявок: {len(self.requests)}",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def refresh_table(self):
        """Обновляет отображение таблицы"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Заполнение таблицы
        for request in self.filtered_requests:
            # Получение имени клиента
            client_name = "Неизвестно"
            if request['client_id']:
                for user in self.users:
                    if user['id'] == request['client_id']:
                        client_name = user['fio']
                        break
            
            # Получение имени механика
            master_name = "Не назначен"
            if request['master_id']:
                for user in self.users:
                    if user['id'] == request['master_id']:
                        master_name = user['fio']
                        break
            
            # Формирование строки автомобиля
            car = f"{request['car_type']} {request['car_model']}"
            
            # Определение цвета строки по статусу
            tags = ()
            if request['status'] == "Готова к выдаче":
                tags = ('completed',)
            elif request['status'] == "В процессе ремонта":
                tags = ('in_progress',)
            
            # Вставка строки
            self.tree.insert(
                '', tk.END,
                values=(
                    request['id'],
                    request['start_date'],
                    client_name,
                    car,
                    request['status'],
                    master_name,
                    request['description'][:50] + '...' if len(request['description']) > 50 else request['description']
                ),
                tags=tags
            )
        
        # Настройка цветов
        self.tree.tag_configure('completed', background='#e8f5e8')  # светло-зеленый
        self.tree.tag_configure('in_progress', background='#fff3e0')  # светло-оранжевый
        
        # Обновление статусной строки
        self.update_status_bar()
        
    def update_status_bar(self):
        """Обновляет строку состояния"""
        total = len(self.requests)
        filtered = len(self.filtered_requests)
        completed = sum(1 for r in self.requests if r['status'] == "Готова к выдаче")
        in_progress = sum(1 for r in self.requests if r['status'] == "В процессе ремонта")
        new = sum(1 for r in self.requests if r['status'] == "Новая заявка")
        
        self.status_bar.config(
            text=f"Всего: {total} | Показано: {filtered} | ✅ Завершено: {completed} | "
                 f"🔄 В работе: {in_progress} | 📋 Новых: {new}"
        )
        
    def sort_column(self, col, reverse):
        """Сортировка по колонке"""
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children('')]
        data.sort(reverse=reverse)
        
        for index, (val, child) in enumerate(data):
            self.tree.move(child, '', index)
        
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))
        
    def get_selected_request(self):
        """Возвращает выбранную заявку"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning(
                "Предупреждение",
                "Выберите заявку из списка!"
            )
            return None
        
        # Получаем ID заявки
        item = self.tree.item(selection[0])
        request_id = int(item['values'][0])
        
        # Находим заявку в списке
        for request in self.requests:
            if request['id'] == request_id:
                return request
        
        return None
        
    def create_request(self):
        """Создание новой заявки"""
        dialog = RequestDialog(self.root, None, self.users, mode='create')
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            # Генерация нового ID
            new_id = max([r['id'] for r in self.requests]) + 1 if self.requests else 1
            
            # Создание новой заявки
            new_request = {
                'id': new_id,
                'start_date': datetime.now().strftime('%Y-%m-%d'),
                'car_type': dialog.result['car_type'],
                'car_model': dialog.result['car_model'],
                'description': dialog.result['description'],
                'status': 'Новая заявка',
                'completion_date': None,
                'repair_parts': '',
                'master_id': None,
                'client_id': dialog.result['client_id']
            }
            
            self.requests.append(new_request)
            self.filtered_requests = self.requests.copy()
            self.refresh_table()
            
            messagebox.showinfo(
                "Успешно",
                f"Заявка №{new_id} успешно создана!"
            )
            
    def edit_request(self):
        """Редактирование заявки"""
        request = self.get_selected_request()
        if not request:
            return
        
        # Проверка прав
        if self.current_user['role'] == 'Автомеханик' and request['master_id'] != self.current_user['id']:
            messagebox.showerror(
                "Ошибка доступа",
                "Вы можете редактировать только свои заявки!"
            )
            return
        
        dialog = RequestDialog(self.root, request, self.users, mode='edit')
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            # Обновление данных
            request.update(dialog.result)
            self.refresh_table()
            
            messagebox.showinfo(
                "Успешно",
                f"Заявка №{request['id']} обновлена!"
            )
            
    def open_comments(self):
        """Открывает окно комментариев"""
        request = self.get_selected_request()
        if not request:
            return
        
        # Проверка прав (только механик)
        if self.current_user['role'] != 'Автомеханик':
            messagebox.showerror(
                "Ошибка доступа",
                "Только автомеханик может просматривать и добавлять комментарии!"
            )
            return
        
        # Проверка, назначен ли механик на заявку
        if request['master_id'] and request['master_id'] != self.current_user['id']:
            messagebox.showerror(
                "Ошибка доступа",
                "Вы можете оставлять комментарии только к своим заявкам!"
            )
            return
        
        # Открываем окно комментариев
        comments_window = CommentsWindow(
            self.root,
            request,
            self.comments,
            self.current_user,
            self.users
        )
        
    def show_statistics(self):
        """Показывает статистику работы"""
        # Расчет статистики
        total_requests = len(self.requests)
        completed_requests = [r for r in self.requests if r['status'] == "Готова к выдаче"]
        completed_count = len(completed_requests)
        
        # Расчет среднего времени ремонта
        total_days = 0
        valid_completed = 0
        
        for req in completed_requests:
            if req['completion_date'] and req['completion_date'] != 'null':
                try:
                    start = datetime.strptime(req['start_date'], '%Y-%m-%d')
                    end = datetime.strptime(req['completion_date'], '%Y-%m-%d')
                    days = (end - start).days
                    if days >= 0:
                        total_days += days
                        valid_completed += 1
                except (ValueError, TypeError):
                    continue
        
        avg_time = total_days / valid_completed if valid_completed > 0 else 0
        
        # Формирование сообщения
        stats_text = f"📊 СТАТИСТИКА РАБОТЫ\n"
        stats_text += f"{'='*40}\n\n"
        stats_text += f"Всего заявок: {total_requests}\n"
        stats_text += f"✅ Выполнено заявок: {completed_count}\n"
        stats_text += f"⏱️ Среднее время ремонта: {avg_time:.1f} дней\n"
        
        messagebox.showinfo("Статистика работы", stats_text)
        
    def apply_filter(self):
        """Применяет фильтр по статусу"""
        status = self.status_filter.get()
        
        if status == "Все":
            self.filtered_requests = self.requests.copy()
        else:
            self.filtered_requests = [r for r in self.requests if r['status'] == status]
        
        self.refresh_table()
        
    def search_requests(self):
        """Поиск заявок по ID или модели"""
        search_text = self.search_entry.get().strip().lower()
        
        if not search_text:
            messagebox.showwarning(
                "Предупреждение",
                "Введите текст для поиска!"
            )
            return
        
        # Поиск по ID или модели
        results = []
        for req in self.requests:
            # Поиск по ID
            if search_text.isdigit() and req['id'] == int(search_text):
                results.append(req)
            # Поиск по модели
            elif search_text in req['car_model'].lower():
                results.append(req)
        
        if results:
            self.filtered_requests = results
            self.refresh_table()
            
            messagebox.showinfo(
                "Результаты поиска",
                f"Найдено заявок: {len(results)}"
            )
        else:
            messagebox.showinfo(
                "Результаты поиска",
                f"По запросу '{search_text}' ничего не найдено.\n"
                "Попробуйте изменить критерии поиска."
            )
            
    def reset_filter(self):
        """Сбрасывает все фильтры"""
        self.status_filter.set("Все")
        self.search_entry.delete(0, tk.END)
        self.filtered_requests = self.requests.copy()
        self.refresh_table()
        
    def show_about(self):
        """Показывает информацию о программе"""
        about_text = """
Программа учёта заявок на ремонт автомобилей
Версия: 1.0
Разработано для демонстрационного экзамена
Вариант №3

© 2026 АвтоТранс
        """
        messagebox.showinfo("О программе", about_text)
        
    def on_closing(self):
        """Обработчик закрытия окна"""
        result = messagebox.askyesno(
            "Выход",
            "Вы уверены, что хотите выйти из программы?",
            icon=messagebox.QUESTION
        )
        if result:
            self.root.quit()