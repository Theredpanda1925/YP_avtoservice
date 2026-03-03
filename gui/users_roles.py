# users_roles.py - Управление пользователями
import sqlite3

def setup_users_and_roles():
    """Настройка пользователей и ролей"""
    
    conn = sqlite3.connect("autoservice.db")
    cursor = conn.cursor()
    
    print("\n" + "="*50)
    print("УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ И РОЛЯМИ")
    print("="*50)
    
    # Текущие пользователи
    print("\n📋 Список пользователей:")
    cursor.execute('''
        SELECT user_id, full_name, user_type, login
        FROM users
        ORDER BY user_type, full_name
    ''')
    
    for user in cursor.fetchall():
        print(f"  [{user[2]}] {user[0]}: {user[1]} (логин: {user[3]})")
    
    # Группы пользователей
    print("\n👥 Группы пользователей:")
    cursor.execute('''
        SELECT user_type, COUNT(*) 
        FROM users 
        GROUP BY user_type
    ''')
    
    for group, count in cursor.fetchall():
        print(f"  • {group}: {count} пользователей")
    
    # Создание новой роли (Менеджер по качеству)
    print("\n🆕 Добавление новой роли 'Менеджер по качеству'...")
    
    # Здесь мы не меняем структуру, просто показываем
    print("  Роль 'Менеджер по качеству' будет добавлена в следующей версии")
    
    conn.close()

if __name__ == "__main__":
    setup_users_and_roles()