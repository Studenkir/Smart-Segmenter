import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, 
    QCheckBox, QSpinBox, QTextEdit, QPushButton, QDateEdit,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox,
    QRadioButton, QButtonGroup, QMessageBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

import json

class DataInputForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Главный layout
        main_layout = QVBoxLayout()
        
        # Заголовок формы
        title = QLabel("ФОРМА ВВОДА ДАННЫХ ДЛЯ AI")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2C3E50; margin: 15px;")
        main_layout.addWidget(title)
        
        # Создаем группировки для разных типов данных
        main_layout.addWidget(self.create_personal_info_group())
        main_layout.addWidget(self.create_ai_settings_group())
        main_layout.addWidget(self.create_exp_settings_group())
        main_layout.addWidget(self.create_data_input_group())
        main_layout.addWidget(self.create_actions_group())
        
        self.setLayout(main_layout)
        self.setWindowTitle("AI Data Input Form")
        self.setGeometry(200, 200, 500, 700)
    
    def create_personal_info_group(self):
        """Группа для персональной информации"""
        group = QGroupBox("1. Персональные данные")
        layout = QGridLayout()
        
        # Строка 0
        layout.addWidget(QLabel("ФИО:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите ваше имя")
        layout.addWidget(self.name_input, 0, 1)
        
        # Строка 1
        layout.addWidget(QLabel("Email:"), 1, 0)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@mail.com")
        layout.addWidget(self.email_input, 1, 1)
        
        # Строка 2
        layout.addWidget(QLabel("Телефон:"), 2, 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("+7 (XXX) XXX-XX-XX")
        layout.addWidget(self.phone_input, 2, 1)
        
        # Строка 3
        layout.addWidget(QLabel("Дата рождения:"), 3, 0)
        self.birth_date = QDateEdit()
        self.birth_date.setDate(QDate(1990, 1, 1))
        self.birth_date.setCalendarPopup(True)
        layout.addWidget(self.birth_date, 3, 1)
        
        # Строка 4
        layout.addWidget(QLabel("Пол:"), 4, 0)
        gender_layout = QHBoxLayout()
        self.gender_male = QRadioButton("Мужской")
        self.gender_female = QRadioButton("Женский")
        self.gender_male.setChecked(True)
        gender_layout.addWidget(self.gender_male)
        gender_layout.addWidget(self.gender_female)
        gender_layout.addStretch()
        layout.addLayout(gender_layout, 4, 1)
        
        group.setLayout(layout)
        return group
    
    def create_ai_settings_group(self):
        """Группа для настроек AI модели"""
        group = QGroupBox("2. Настройки AI модели")
        layout = QGridLayout()
        
        # Строка 0
        layout.addWidget(QLabel("Тип модели:"), 0, 0)
        self.model_type = QComboBox()
        self.model_type.addItems([
            "Нейронная сеть", 
            "Random Forest", 
            "SVM", 
            "K-Means",
            "Градиентный бустинг"
        ])
        layout.addWidget(self.model_type, 0, 1)
        
        # Строка 1
        layout.addWidget(QLabel("Количество эпох:"), 1, 0)
        self.epochs_spin = QSpinBox()
        self.epochs_spin.setRange(1, 1000)
        self.epochs_spin.setValue(100)
        layout.addWidget(self.epochs_spin, 1, 1)
        
        # Строка 2
        layout.addWidget(QLabel("Размер батча:"), 2, 0)
        self.batch_size = QComboBox()
        self.batch_size.addItems(["16", "32", "64", "128", "256"])
        self.batch_size.setCurrentText("32")
        layout.addWidget(self.batch_size, 2, 1)
        
        # Строка 3
        layout.addWidget(QLabel("Оптимизатор:"), 3, 0)
        self.optimizer = QComboBox()
        self.optimizer.addItems(["Adam", "SGD", "RMSprop", "Adagrad"])
        layout.addWidget(self.optimizer, 3, 1)
        
        # Строка 4 - чекбоксы
        options_layout = QHBoxLayout()
        self.normalize_data = QCheckBox("Нормализация данных")
        self.augment_data = QCheckBox("Аугментация данных")
        self.normalize_data.setChecked(True)
        options_layout.addWidget(self.normalize_data)
        options_layout.addWidget(self.augment_data)
        options_layout.addStretch()
        layout.addWidget(QLabel("Доп. опции:"), 4, 0)
        layout.addLayout(options_layout, 4, 1)
        
        group.setLayout(layout)
        return group
    
    def create_exp_settings_group(self):
        """Экспериментальные настройки"""
        group = QGroupBox("Экспериментальные настройки")
        layout = QGridLayout()
        
        # Строка 0
        layout.addWidget(QLabel("Скорость обучения:"), 0, 0)
        self.regularization = QDoubleSpinBox()
        layout.addWidget(self.regularization, 0, 1)

        # Строка 1
        layout.addWidget(QLabel("Регуляризация:"), 1, 0)
        self.regularization = QComboBox()
        self.regularization.addItems([
            "L1", "L2", "None"
        ])
        layout.addWidget(self.regularization, 1, 1)
        
        # Строка 3 Ранняя остановка
        options_layout = QHBoxLayout()
        self.early_stop = QCheckBox()
        self.early_stop.setChecked(False)
        options_layout.addWidget(self.early_stop)
        options_layout.addStretch()
        layout.addWidget(QLabel("Ранняя остановка:"), 2, 0)
        layout.addLayout(options_layout, 2, 1)
        
        group.setLayout(layout)
        return group
    
    def create_data_input_group(self):
        """Группа для ввода данных"""
        group = QGroupBox("3. Ввод данных для анализа")
        layout = QVBoxLayout()
        
        # Область для ввода текста
        layout.addWidget(QLabel("Текст для анализа:"))
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Введите текст для обработки AI моделью...")
        self.text_input.setMaximumHeight(100)
        layout.addWidget(self.text_input)
        
        # Числовые параметры
        params_layout = QGridLayout()
        params_layout.addWidget(QLabel("Параметр A:"), 0, 0)
        self.param_a = QSpinBox()
        self.param_a.setRange(0, 100)
        params_layout.addWidget(self.param_a, 0, 1)
        
        params_layout.addWidget(QLabel("Параметр B:"), 1, 0)
        self.param_b = QSpinBox()
        self.param_b.setRange(0, 100)
        params_layout.addWidget(self.param_b, 1, 1)
        
        params_layout.addWidget(QLabel("Параметр C:"), 2, 0)
        self.param_c = QSpinBox()
        self.param_c.setRange(0, 100)
        params_layout.addWidget(self.param_c, 2, 1)
        
        layout.addLayout(params_layout)
        group.setLayout(layout)
        return group
    
    def create_actions_group(self):
        """Группа с кнопками действий"""
        group = QGroupBox("4. Действия")
        layout = QHBoxLayout()
        
        # Кнопка отправки
        self.submit_btn = QPushButton("📊 Отправить данные")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        self.submit_btn.clicked.connect(self.submit_data)
        
        # Кнопка очистки
        self.clear_btn = QPushButton("🗑️ Очистить форму")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_form)
        
        layout.addWidget(self.submit_btn)
        layout.addWidget(self.clear_btn)
        
        group.setLayout(layout)
        return group
    
    def submit_data(self):
        """Обработчик отправки формы"""
        # Проверка обязательных полей
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Поле 'ФИО' обязательно для заполнения!")
            return
        
        if not self.email_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Поле 'Email' обязательно для заполнения!")
            return

        if "@" not in self.email_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Поле 'Email' некорректно!")
            return
        
        # Сбор данных из формы
        data = {
            "personal_info": {
                "name": self.name_input.text(),
                "email": self.email_input.text(),
                "phone": self.phone_input.text(),
                "birth_date": self.birth_date.date().toString("dd.MM.yyyy"),
                "gender": "Мужской" if self.gender_male.isChecked() else "Женский"
            },
            "ai_settings": {
                "model_type": self.model_type.currentText(),
                "epochs": self.epochs_spin.value(),
                "batch_size": self.batch_size.currentText(),
                "optimizer": self.optimizer.currentText(),
                "normalize_data": self.normalize_data.isChecked(),
                "augment_data": self.augment_data.isChecked()
            },
            "input_data": {
                "text": self.text_input.toPlainText(),
                "param_a": self.param_a.value(),
                "param_b": self.param_b.value(),
                "param_c": self.param_c.value()
            }
        }
        with open("data_json_ex2.json", "w") as f:
            json.dump(data, f)

        # Вывод собранных данных (в реальном приложении здесь была бы отправка на сервер)
        print("Данные формы:", data)
        
        QMessageBox.information(
            self, 
            "Успех!", 
            "Данные успешно отправлены!\n\n"
            f"Модель: {data['ai_settings']['model_type']}\n"
            f"Эпох: {data['ai_settings']['epochs']}\n"
            f"Текст для анализа: {len(data['input_data']['text'])} символов"
        )
    
    def clear_form(self):
        """Очистка формы"""
        reply = QMessageBox.question(
            self, 
            "Подтверждение", 
            "Вы уверены, что хотите очистить все поля формы?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Очищаем все поля
            self.name_input.clear()
            self.email_input.clear()
            self.phone_input.clear()
            self.birth_date.setDate(QDate(1990, 1, 1))
            self.gender_male.setChecked(True)
            
            self.model_type.setCurrentIndex(0)
            self.epochs_spin.setValue(100)
            self.batch_size.setCurrentText("32")
            self.optimizer.setCurrentIndex(0)
            self.normalize_data.setChecked(True)
            self.augment_data.setChecked(False)
            
            self.text_input.clear()
            self.param_a.setValue(0)
            self.param_b.setValue(0)
            self.param_c.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль для всего приложения
    app.setStyle('Fusion')
    
    window = DataInputForm()
    window.show()
    
    sys.exit(app.exec())
