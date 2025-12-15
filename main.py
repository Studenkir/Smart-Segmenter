import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QStackedWidget, QLabel, QStatusBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

from admin_screen import AdminScreen
from profiles_screen import ProfilesScreen
from data_analyzer import DataAnalyzer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smart Segmenter - Прототип")
        self.setGeometry(100, 100, 1200, 700)
        
        # Центральный виджет и основной layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Создаем навигационную панель слева
        self.nav_layout = QVBoxLayout()
        self.create_navigation()
        main_layout.addLayout(self.nav_layout)
        
        # Создаем область контента справа
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, stretch=4)
        
        # Создаем экраны
        self.create_screens()
        
        # Создаем меню и статусбар
        self.create_menu()
        self.create_statusbar()
        
        # Показываем начальный экран
        self.show_diagram_screen()

    def create_navigation(self):
        """Создает панель навигации"""
        nav_label = QLabel("Навигация")
        nav_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nav_label.setStyleSheet("font-weight: bold; font-size: 14pt; margin: 10px;")
        self.nav_layout.addWidget(nav_label)
        
        # Кнопки навигации
        self.diagram_btn = QPushButton("📊 Диаграммы")
        self.profiles_btn = QPushButton("📑 Профили клиентов")
        self.admin_btn = QPushButton("⚙️ Админ-панель")
        
        # Стилизация кнопок
        nav_buttons = [self.diagram_btn, self.profiles_btn, self.admin_btn]
        for btn in nav_buttons:
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 10px;
                    border: none;
                    background-color: #f0f0f0;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
            """)
            self.nav_layout.addWidget(btn)
        
        # Подключаем обработчики
        self.diagram_btn.clicked.connect(self.show_diagram_screen)
        self.profiles_btn.clicked.connect(self.show_profiles_screen)
        self.admin_btn.clicked.connect(self.show_admin_screen)
        
        self.nav_layout.addStretch()

    def create_screens(self):
        """Создает экраны приложения"""
        # Экран с диаграммами
        self.diagram_screen = DataAnalyzer()
        
        # Экран с профилями клиентов
        self.profiles_screen = ProfilesScreen()
        
        # Экран админки
        self.admin_screen = AdminScreen()
        
        # Добавляем экраны в стек
        self.content_stack.addWidget(self.diagram_screen)
        self.content_stack.addWidget(self.profiles_screen)
        self.content_stack.addWidget(self.admin_screen)

    def create_menu(self):
        """Создает строку меню"""
        menubar = self.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        
        exit_action = QAction("Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Меню Вид
        view_menu = menubar.addMenu("Вид")
        
        feed_action = QAction("Диаграммы", self)
        feed_action.triggered.connect(self.show_diagram_screen)
        view_menu.addAction(feed_action)
        
        interests_action = QAction("Профили", self)
        interests_action.triggered.connect(self.show_profiles_screen)
        view_menu.addAction(interests_action)

    def create_statusbar(self):
        """Создает статусбар"""
        statusbar = QStatusBar()
        statusbar.showMessage("Готов к работе")
        self.setStatusBar(statusbar)

    def show_diagram_screen(self):
        """Показывает экран с диаграммами"""
        self.content_stack.setCurrentWidget(self.diagram_screen)
        self.update_status("Просмотр диаграмм")

    def show_profiles_screen(self):
        """Показывает экран профилей"""
        self.content_stack.setCurrentWidget(self.profiles_screen)
        self.update_status("Просмотр профилей")

    def show_admin_screen(self):
        """Показывает экран админки"""
        self.content_stack.setCurrentWidget(self.admin_screen)
        self.update_status("Административная панель")

    def update_status(self, message):
        """Обновляет статусбар"""
        self.statusBar().showMessage(f"{message} | Smart Segmenter Prototype")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()