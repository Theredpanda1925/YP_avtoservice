# gui/request_dialog.py - Диалог создания/редактирования заявки
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class RequestDialog:
    def __init__(self, parent, request, users, mode='create'):
        self.result = None
        self.request = request
        self.users = users
        self.mode = mode
        
        # Создание диалогового окна
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"{'Новая заявка' if mode == 'create' else f'Редактирование заявки №{request["id"]}'}")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Центрирование окна
        self.center_window()
        
        # Создание виджетов
        self.create_widgets()
        
        # Заполнение данных при редактировании
        if mode == 'edit' and request:
            self.fill_data()
            
    def center_window(self):
        """Центрирует окно относительно родителя"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = self.dialog.winfo_screenwidth() // 2 - width // 2
        y = self.dialog.winfo_screenheight() // 2 - height // 2
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Создает элементы интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        row = 0
        
        # Клиент
        ttk.Label(main_frame, text="Клиент:*", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        
        # Получаем список клиентов
        self.clients = [u for u in self.users if u['role'] == 'Заказчик']
        client_names = [f"{c['id']}: {c['fio']} ({c['phone']})" for c in self.clients]
        
        self.client_var = tk.StringVar()
        self.client_combo = ttk.Combobox(
            main_frame,
            textvariable=self.client_var,
            values=client_names,
            state='readonly',
            width=40
        )
        self.client_combo.grid(row=row, column=1, columnspan=2, pady=5, sticky=tk.W)
        row += 1
        
        # Вид авто
        ttk.Label(main_frame, text="Вид авто:*", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.car_type = ttk.Combobox(
            main_frame,
            values=['Легковая', 'Грузовая', 'Автобус', 'Мотоцикл'],
            state='readonly',
            width=38
        )
        self.car_type.grid(row=row, column=1, columnspan=2, pady=5, sticky=tk.W)
        row += 1
        
        # Модель авто
        ttk.Label(main_frame, text="Модель авто:*", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.car_model = ttk.Entry(main_frame, width=40)
        self.car_model.grid(row=row, column=1, columnspan=2, pady=5, sticky=tk.W)
        row += 1
        
        # Описание проблемы
        ttk.Label(main_frame, text="Описание проблемы:*", font=('Arial', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5
        )
        self.description = tk.Text(main_frame, width=40, height=5)
        self.description.grid(row=row, column=1, columnspan=2, pady=5, sticky=tk.W)
        row += 1
        
        # Статус (только для редактирования)
        if self.mode == 'edit':
            ttk.Label(main_frame, text="Статус:", font=('Arial', 10, 'bold')).grid(
                row=row, column=0, sticky=tk.W, pady=5
            )
            self.status = ttk.Combobox(
                main_frame,
                values=['Новая заявка', 'В процессе ремонта', 'Готова к выдаче'],
                state='readonly',
                width=38
            )
            self.status.grid(row=row, column=1, columnspan=2, pady=5, sticky=tk.W)
            row += 1
            
            # Дата завершения
            ttk.Label(main_frame, text="Дата завершения:").grid(
                row=row, column=0, sticky=tk.W, pady=5
            )
            self.completion_date = ttk.Entry(main_frame, width=40)
            self.completion_date.grid(row=row, column=1, columnspan=2, pady=5, sticky=tk.W)
            row += 1
            
            # Механик
            ttk.Label(main_frame, text="Ответственный механик:").grid(
                row=row, column=0, sticky=tk.W, pady=5
            )
            # Получаем список механиков
            self.mechanics = [u for u in self.users if u['role'] == 'Автомеханик']
            mechanic_names = [f"{m['id']}: {m['fio']}" for m in self.mechanics]
            mechanic_names.insert(0, "Не назначен")
            
            self.master_var = tk.StringVar()
            self.master_combo = ttk.Combobox(
                main_frame,
                textvariable=self.master_var,
                values=mechanic_names,
                state='readonly',
                width=38
            )
            self.master_combo.grid(row=row, column=1, columnspan=2, pady=5, sticky=tk.W)
            row += 1
            
            # Запчасти
            ttk.Label(main_frame, text="Заказанные запчасти:").grid(
                row=row, column=0, sticky=tk.W, pady=5
            )
            self.repair_parts = tk.Text(main_frame, width=40, height=3)
            self.repair_parts.grid(row=row, column=1, columnspan=2, pady=5, sticky=tk.W)
            row += 1
        
        # Подпись об обязательных полях
        ttk.Label(
            main_frame,
            text="* - обязательные поля",
            foreground='gray'
        ).grid(row=row, column=0, columnspan=3, pady=10)
        row += 1
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        ttk.Button(
            button_frame,
            text="Сохранить",
            command=self.save,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Отмена",
            command=self.cancel,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
    def fill_data(self):
        """Заполняет поля данными при редактировании"""
        # Выбор клиента
        for i, client in enumerate(self.clients):
            if client['id'] == self.request['client_id']:
                self.client_combo.current(i)
                break
        
        # Вид авто
        self.car_type.set(self.request['car_type'])
        
        # Модель
        self.car_model.insert(0, self.request['car_model'])
        
        # Описание
        self.description.insert('1.0', self.request['description'])
        
        # Статус
        self.status.set(self.request['status'])
        
        # Дата завершения
        if self.request.get('completion_date') and self.request['completion_date'] != 'null':
            self.completion_date.insert(0, self.request['completion_date'])
        
        # Механик
        if self.request['master_id']:
            for i, mech in enumerate(self.mechanics):
                if mech['id'] == self.request['master_id']:
                    self.master_combo.current(i + 1)  # +1 из-за "Не назначен"
                    break
        else:
            self.master_combo.current(0)
        
        # Запчасти
        if self.request.get('repair_parts'):
            self.repair_parts.insert('1.0', self.request['repair_parts'])
        
    def validate(self):
        """Проверяет заполнение обязательных полей"""
        if not self.client_var.get():
            messagebox.showwarning(
                "Предупреждение",
                "Выберите клиента!"
            )
            return False
        
        if not self.car_type.get():
            messagebox.showwarning(
                "Предупреждение",
                "Выберите вид автомобиля!"
            )
            return False
        
        if not self.car_model.get().strip():
            messagebox.showwarning(
                "Предупреждение",
                "Введите модель автомобиля!"
            )
            return False
        
        if not self.description.get('1.0', tk.END).strip():
            messagebox.showwarning(
                "Предупреждение",
                "Введите описание проблемы!"
            )
            return False
        
        return True
        
    def save(self):
        """Сохраняет данные"""
        if not self.validate():
            return
        
        # Получение ID клиента
        client_text = self.client_var.get()
        client_id = int(client_text.split(':')[0])
        
        # Формирование результата
        result = {
            'client_id': client_id,
            'car_type': self.car_type.get(),
            'car_model': self.car_model.get().strip(),
            'description': self.description.get('1.0', tk.END).strip()
        }
        
        # Добавление полей для редактирования
        if self.mode == 'edit':
            result['status'] = self.status.get()
            
            completion_date = self.completion_date.get().strip()
            result['completion_date'] = completion_date if completion_date else None
            
            # Получение ID механика
            master_text = self.master_var.get()
            if master_text and master_text != "Не назначен":
                result['master_id'] = int(master_text.split(':')[0])
            else:
                result['master_id'] = None
            
            result['repair_parts'] = self.repair_parts.get('1.0', tk.END).strip()
        
        self.result = result
        self.dialog.destroy()
        
    def cancel(self):
        """Отмена"""
        if messagebox.askyesno(
            "Подтверждение",
            "Отменить изменения? Все несохранённые данные будут потеряны."
        ):
            self.dialog.destroy()