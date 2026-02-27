# data_manager.py - Модуль для работы с данными
import csv
from datetime import datetime

class DataManager:
    """Класс для загрузки данных из файлов"""
    
    @staticmethod
    def load_users(filepath):
        """Загружает пользователей из файла"""
        users = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                # Читаем заголовок
                header = file.readline().strip().split(';')
                print(f"Заголовок users: {header}")
                
                for line_num, line in enumerate(file, start=2):
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split(';')
                    if len(parts) >= 6:
                        try:
                            user = {
                                'id': int(parts[0]),
                                'fio': parts[1],
                                'phone': parts[2],
                                'login': parts[3],
                                'password': parts[4],
                                'role': parts[5]
                            }
                            users.append(user)
                            print(f"Загружен пользователь: {user['fio']} - {user['role']}")
                        except ValueError as e:
                            print(f"Ошибка в строке {line_num}: {e}")
        except FileNotFoundError:
            print(f"ОШИБКА: Файл {filepath} не найден!")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
        
        return users
    
    @staticmethod
    def load_requests(filepath):
        """Загружает заявки из файла"""
        requests = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                # Читаем заголовок
                header = file.readline().strip().split(';')
                print(f"Заголовок requests: {header}")
                
                for line_num, line in enumerate(file, start=2):
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split(';')
                    if len(parts) >= 10:
                        try:
                            # Обработка пустых значений
                            completion_date = parts[6] if len(parts) > 6 and parts[6] != 'null' else None
                            repair_parts = parts[7] if len(parts) > 7 and parts[7] else ''
                            
                            # Обработка master_id
                            master_id = None
                            if len(parts) > 8 and parts[8] and parts[8] != 'null':
                                try:
                                    master_id = int(parts[8])
                                except:
                                    master_id = None
                            
                            # Обработка client_id
                            client_id = None
                            if len(parts) > 9 and parts[9]:
                                try:
                                    client_id = int(parts[9])
                                except:
                                    client_id = None
                            
                            request = {
                                'id': int(parts[0]),
                                'start_date': parts[1],
                                'car_type': parts[2],
                                'car_model': parts[3],
                                'description': parts[4],
                                'status': parts[5],
                                'completion_date': completion_date,
                                'repair_parts': repair_parts,
                                'master_id': master_id,
                                'client_id': client_id
                            }
                            requests.append(request)
                            print(f"Загружена заявка {request['id']}: {request['car_model']} - {request['status']}")
                        except (ValueError, IndexError) as e:
                            print(f"Ошибка в строке {line_num}: {e}, данные: {parts}")
        except FileNotFoundError:
            print(f"ОШИБКА: Файл {filepath} не найден!")
        
        return requests
    
    @staticmethod
    def load_comments(filepath):
        """Загружает комментарии из файла"""
        comments = []
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                # Читаем заголовок
                header = file.readline().strip().split(';')
                print(f"Заголовок comments: {header}")
                
                for line_num, line in enumerate(file, start=2):
                    line = line.strip()
                    if not line:
                        continue
                    
                    parts = line.split(';')
                    if len(parts) >= 4:
                        try:
                            comment = {
                                'id': int(parts[0]),
                                'message': parts[1],
                                'master_id': int(parts[2]),
                                'request_id': int(parts[3])
                            }
                            comments.append(comment)
                            print(f"Загружен комментарий {comment['id']} к заявке {comment['request_id']}")
                        except (ValueError, IndexError) as e:
                            print(f"Ошибка в строке {line_num}: {e}")
        except FileNotFoundError:
            print(f"ОШИБКА: Файл {filepath} не найден!")
        
        return comments