from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
                             QLabel, QPushButton, QFrame, QSizePolicy, QLineEdit)
from PyQt6.QtCore import Qt
import pandas as pd

from ml_models import MLModels

class ProfilesScreen(QFrame):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.full_list = []
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # Увеличиваем расстояние между элементами
        layout.setContentsMargins(10, 10, 10, 10)  # Добавляем отступы от краев

        # Заголовок
        title = QLabel("--> Профили клиентов <--")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; margin: 8px;")
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(title)
        
        # Кнопка добавления нового элемента
        add_button = QPushButton("🔄 Обновить профили")
        add_button.clicked.connect(self.add_profils)
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #4acd32; 
                color: white; 
                border: none; 
                padding: 8px; 
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2fdb24;
            }
        """)
        
        add_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        layout.addWidget(add_button)
        
        # Прокручиваемая область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Контейнер для элементов
        self.container = QWidget()  # Делаем контейнер атрибутом класса
        self.container_layout = QVBoxLayout(self.container)  # И его layout тоже
        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container_layout.setSpacing(5)
        
        # Кнопка очистки
        #clear_btn = QPushButton("Очистить все")
        #clear_btn.clicked.connect(self.clear_all)
        #layout.addWidget(clear_btn)
        
        scroll_area.setWidget(self.container)
        layout.addWidget(scroll_area)
        
        # Счетчик элементов
        self.item_counter = 0
        
    def add_profils(self):
        """Добавляет информацию о профилях"""
        self.clear_all()
        a = MLModels()
        cluster_summary, variables, clusters_info = a.load_profiles(['age', 'experience',
                                'income', 'family', 'mortgage', 'personal_loan', 'creditcard'])
        self.add_variables(variables)
        self.add_summary(cluster_summary)
        self.add_clusters_info(clusters_info)
        
    def add_variables(self, variables):
        """Добавляет список переменных"""
        self.item_counter += 1
        # Создаем layout для элемента
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(5, 2, 5, 2)
        
        display_text = ', '.join(variables)
        
        label = QLabel(f'При сегментации клиентов были использованы следующие данные: {display_text}')
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        label.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: #f9f9f9;
            }
        """)
        item_layout.addWidget(label, 1)  
        # Добавляем элемент в контейнер
        self.container_layout.addWidget(item_widget)
        return item_widget
    
    def add_summary(self, cluster_summary):
        """Добавляет суммаризацию"""
        self.item_counter += 1

        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(5, 2, 5, 2)
        
        if isinstance(cluster_summary, pd.DataFrame):
            display_text = cluster_summary.to_string()
        else:
            display_text = str(cluster_summary)
        
        label = QLabel(display_text)
        label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        label.setStyleSheet("""
            QLabel {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: #f9f9f9;
            }
        """)
        item_layout.addWidget(label, 1)
        self.container_layout.addWidget(item_widget)
        return item_widget
    
    def add_clusters_info(self, clusters_info):
        """Добавляет доп инфу о кластерах"""
        for cluster_num, info in clusters_info.items():
            text_0 = info[0]
            text_1 = f"Информация о профиле №{cluster_num}: {info[1]} клиентов, {round(int(info[2]), 2)}%"
            self.for_clusters_info(text_0, text_1)
    
    def for_clusters_info(self, text_0: str, text_1: str):
        """Добавляет доп инфу о кластерах"""
        self.item_counter += 1
        
        item_widget = QWidget()
        item_layout = QVBoxLayout(item_widget)
        item_layout.setContentsMargins(5, 2, 5, 2)
        
        button = QPushButton("✏️ Изменить описание")
        button.setStyleSheet("""
            QPushButton {
                background-color: #4acd32; 
                color: white; 
                border: none; 
                padding: 6px; 
                border-radius: 3px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2fdb24;
            }
        """)
        button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        line_edit = QLineEdit()
        line_edit.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        label_1 = QLabel(text_1)
        label_0 = QLabel(text_0)
        label_0.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        item_layout.addWidget(button)
        item_layout.addWidget(line_edit)
        item_layout.addWidget(label_1)
        item_layout.addWidget(label_0)

        def update_label():
            text = line_edit.text()
            label_0.setText(text)

        button.clicked.connect(update_label)

        self.container_layout.addWidget(item_widget)
        return item_widget
        
        
    def clear_all(self):
        """Очищает все элементы"""
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self.item_counter = 0