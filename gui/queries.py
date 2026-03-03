# queries.py - Запросы для отчетов (ЗАДАНИЕ 2.5)
import sqlite3
from datetime import datetime

def run_queries():
    """Выполняет все необходимые запросы для отчета"""
    
    conn = sqlite3.connect("autoservice.db")
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("ОТЧЕТЫ ПО ЗАЯВКАМ НА РЕМОНТ")
    print("="*60)
    
    # 1. Количество выполненных заявок
    cursor.execute('''
        SELECT COUNT(*) FROM requests 
        WHERE status = 'Готова к выдаче' OR status = 'Завершена'
    ''')
    completed = cursor.fetchone()[0]
    print(f"\n1. Количество выполненных заявок: {completed}")
    
    # 2. Среднее время выполнения
    cursor.execute('''
        SELECT AVG(
            julianday(completion_date) - julianday(start_date)
        ) FROM requests 
        WHERE completion_date IS NOT NULL 
          AND completion_date != 'null'
    ''')
    avg_time = cursor.fetchone()[0]
    print(f"2. Среднее время выполнения: {avg_time:.1f} дней")
    
    # 3. Статистика по типам неисправностей
    print("\n3. Статистика по типам неисправностей:")
    
    # Тормозная система
    cursor.execute('''
        SELECT COUNT(*) FROM requests 
        WHERE description LIKE '%тормоз%'
    ''')
    brakes = cursor.fetchone()[0]
    print(f"   • Тормозная система: {brakes} заявок")
    
    # Двигатель
    cursor.execute('''
        SELECT COUNT(*) FROM requests 
        WHERE description LIKE '%бензин%' 
           OR description LIKE '%двигатель%'
    ''')
    engine = cursor.fetchone()[0]
    print(f"   • Двигатель: {engine} заявок")
    
    # Рулевое управление
    cursor.execute('''
        SELECT COUNT(*) FROM requests 
        WHERE description LIKE '%рул%'
    ''')
    steering = cursor.fetchone()[0]
    print(f"   • Рулевое управление: {steering} заявок")
    
    # 4. Заявки по статусам
    print("\n4. Заявки по статусам:")
    cursor.execute('''
        SELECT status, COUNT(*) as count 
        FROM requests 
        GROUP BY status
        ORDER BY count DESC
    ''')
    for status, count in cursor.fetchall():
        print(f"   • {status}: {count}")
    
    # 5. Заявки по механикам
    print("\n5. Загрузка механиков:")
    cursor.execute('''
        SELECT u.full_name, COUNT(r.request_id) as requests
        FROM users u
        LEFT JOIN requests r ON u.user_id = r.master_id
        WHERE u.user_type = 'Автомеханик'
        GROUP BY u.user_id
        ORDER BY requests DESC
    ''')
    for mech, count in cursor.fetchall():
        print(f"   • {mech}: {count} заявок")
    
    # 6. Детальный отчет (JOIN)
    print("\n6. Детальный отчет по заявкам:")
    cursor.execute('''
        SELECT 
            r.request_id as "Номер",
            r.start_date as "Дата",
            u.full_name as "Клиент",
            r.car_type || ' ' || r.car_model as "Автомобиль",
            r.description as "Проблема",
            r.status as "Статус",
            m.full_name as "Механик"
        FROM requests r
        JOIN users u ON r.client_id = u.user_id
        LEFT JOIN users m ON r.master_id = m.user_id
        ORDER BY r.request_id
        LIMIT 10
    ''')
    
    for row in cursor.fetchall():
        print(f"   #{row[0]}: {row[1]} | {row[2]} | {row[3]} | {row[5]}")
    
    conn.close()
    
    print("\n" + "="*60)

if __name__ == "__main__":
    run_queries()