import pandas as pd

"""
Модуль для обращения к датасету, часть данных сгенерирована
"""

class ExtractData:
    def __init__(self):
        self.metrics = self.generate_metrics()
        self.info = self.generate_info_clients()
    
    def generate_info_clients(self):
        """Генерирует информацию о клиентах"""
        return [
            {"id": 1, "name": "Ксения", "surname": 'Дмитриева', "patronymic": "Артёмовна"},
            {"id": 1, "name": "Ярослав", "surname": 'Корнилов', "patronymic": "Евгеньевич"},
            {"id": 1, "name": "Алексей", "surname": 'Ермолов', "patronymic": "Денисович"},
            {"id": 1, "name": "Михаил", "surname": 'Борисов', "patronymic": "Ярославович"},
            {"id": 1, "name": "Полина", "surname": 'Белова', "patronymic": "Романовна"}
        ]
    
    def generate_metrics(self):
        """Генерирует тестовые метрики системы"""
        return {
            "precision": 0.78,
            "recall": 0.72,
            "f1_score": 0.75,
            "active_users": 1542,
            "articles_processed": 12547,
            "avg_reading_time": "3.2 мин"
        }

# Создаем глобальный экземпляр для использования в приложении
extract_data = ExtractData()