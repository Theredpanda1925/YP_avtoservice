import sqlite3
import os

def create_database():
    """Создает базу данных из ваших файлов"""
    
    print("="*50)
    print("СОЗДАНИЕ БАЗЫ ДАННЫХ ДЛЯ МОДУЛЯ 2")
    print("="*50)
    
    # Удаляем старую БД если есть
    if os.path.exists("autoservice.db"):
        os.remove("autoservice.db")
        print("🗑️ Удалена старая БД")
    
    # Подключаемся к новой БД
    conn = sqlite3.connect("autoservice.db")
    cursor = conn.cursor()
    
    print("📦 Создание таблиц...")
    
    # Создание таблиц (3НФ)
    cursor.executescript('''
        -- Таблица пользователей
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL
        );
        
        -- Таблица заявок
        CREATE TABLE requests (
            request_id INTEGER PRIMARY KEY,
            start_date TEXT NOT NULL,
            car_type TEXT NOT NULL,
            car_model TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL,
            completion_date TEXT,
            repair_parts TEXT,
            master_id INTEGER,
            client_id INTEGER,
            FOREIGN KEY (master_id) REFERENCES users(user_id),
            FOREIGN KEY (client_id) REFERENCES users(user_id)
        );
        
        -- Таблица комментариев
        CREATE TABLE comments (
            comment_id INTEGER PRIMARY KEY,
            message TEXT NOT NULL,
            master_id INTEGER NOT NULL,
            request_id INTEGER NOT NULL,
            FOREIGN KEY (master_id) REFERENCES users(user_id),
            FOREIGN KEY (request_id) REFERENCES requests(request_id)
        );
        
        -- Индексы для быстрого поиска
        CREATE INDEX idx_requests_status ON requests(status);
        CREATE INDEX idx_requests_master ON requests(master_id);
        CREATE INDEX idx_requests_client ON requests(client_id);
        CREATE INDEX idx_comments_request ON comments(request_id);
    ''')
    
    print("📥 Загрузка данных из ваших файлов...")
    
    # Загрузка пользователей из вашего файла
    with open("inputDataUsers.txt", "r", encoding="utf-8") as f:
        next(f)  # Пропускаем заголовок
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(';')
                cursor.execute('''
                    INSERT INTO users (user_id, full_name, phone, login, password, user_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (int(parts[0]), parts[1], parts[2], parts[3], parts[4], parts[5]))
    
    print(f"  ✅ Загружено пользователей: {cursor.rowcount}")
    
    # Загрузка заявок из вашего файла
    with open("inputDataRequests.txt", "r", encoding="utf-8") as f:
        next(f)  # Пропускаем заголовок
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(';')
                master = int(parts[8]) if parts[8] != 'null' else None
                cursor.execute('''
                    INSERT INTO requests (
                        request_id, start_date, car_type, car_model, 
                        description, status, completion_date, repair_parts,
                        master_id, client_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(parts[0]), parts[1], parts[2], parts[3], 
                    parts[4], parts[5], parts[6] if parts[6] != 'null' else None,
                    parts[7], master, int(parts[9])
                ))
    
    print(f"  ✅ Загружено заявок: {cursor.rowcount}")
    
    # Загрузка комментариев из вашего файла
    with open("inputDataComments.txt", "r", encoding="utf-8") as f:
        next(f)  # Пропускаем заголовок
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(';')
                cursor.execute('''
                    INSERT INTO comments (comment_id, message, master_id, request_id)
                    VALUES (?, ?, ?, ?)
                ''', (int(parts[0]), parts[1], int(parts[2]), int(parts[3])))
    
    print(f"  ✅ Загружено комментариев: {cursor.rowcount}")
    
    conn.commit()
    
    # Проверка
    print("\n🔍 Проверка базы данных:")
    
    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"  Пользователей: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM requests")
    print(f"  Заявок: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT COUNT(*) FROM comments")
    print(f"  Комментариев: {cursor.fetchone()[0]}")
    
    # Пример JOIN запроса
    print("\n📊 Пример запроса (заявки с клиентами):")
    cursor.execute('''
        SELECT r.request_id, r.car_model, r.status, 
               u.full_name as client, m.full_name as mechanic
        FROM requests r
        JOIN users u ON r.client_id = u.user_id
        LEFT JOIN users m ON r.master_id = m.user_id
        LIMIT 5
    ''')
    
    for row in cursor.fetchall():
        print(f"  Заявка {row[0]}: {row[1]} - {row[2]} | Клиент: {row[3]} | Механик: {row[4] or 'не назначен'}")
    
    conn.close()
    
    print("\n" + "="*50)
    print("✅ БАЗА ДАННЫХ УСПЕШНО СОЗДАНА!")
    print(f"📁 Файл: {os.path.abspath('autoservice.db')}")
    print("="*50)

if __name__ == "__main__":
    create_database()