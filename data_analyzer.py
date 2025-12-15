from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QGroupBox, QSpinBox, QMessageBox,
                             QSizePolicy, QComboBox)
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
import matplotlib.pyplot as plt 

class DataAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.initUI()
        
    def initUI(self):
        # Основной layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)  # Увеличиваем расстояние между элементами
        main_layout.setContentsMargins(10, 10, 10, 10)  # Добавляем отступы от краев
        
        # Заголовок
        title = QLabel("--> Анализ данных <--")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; margin: 8px;")
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        main_layout.addWidget(title)
        
        # Панель управления
        control_panel = QGroupBox("🔨 Управление данными")
        control_layout = QHBoxLayout()
        
        # Кнопки загрузки данных
        self.load_btn = QPushButton('🔄 Обновить данные')
        self.load_btn.clicked.connect(self.load_data)
        control_layout.addWidget(self.load_btn)
        
        # Статистика данных
        self.stats_label = QLabel('Данные не загружены')
        control_layout.addWidget(self.stats_label)
        
        control_layout.addStretch()
        control_panel.setLayout(control_layout)
        main_layout.addWidget(control_panel)
        
        # Панель визуализации
        viz_panel = QGroupBox("👁️‍🗨️ Визуализация данных")
        viz_layout = QVBoxLayout()
        
        # Выбор типа графика
        chart_type_layout = QHBoxLayout()
        chart_type_layout.addWidget(QLabel('📊 Тип графика:'))
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(['Гистограмма', 'Диаграмма рассеяния', 'Boxplot'])
        self.chart_type_combo.currentIndexChanged.connect(self.update_chart_options)
        chart_type_layout.addWidget(self.chart_type_combo)
        
        chart_type_layout.addStretch()
        viz_layout.addLayout(chart_type_layout)
        
        # Панель параметров графика
        self.params_panel = QWidget()
        self.params_layout = QHBoxLayout(self.params_panel)
        viz_layout.addWidget(self.params_panel)
        
        # Виджет для matplotlib        
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        # Добавляем панель инструментов matplotlib
        viz_layout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas)
        viz_layout.addWidget(self.toolbar)
        
        viz_panel.setLayout(viz_layout)
        main_layout.addWidget(viz_panel)
        
        # Информационная панель
        info_panel = QGroupBox("📩 Информация")
        info_layout = QHBoxLayout()
        
        self.info_label = QLabel('Выберите тип графика и параметры для визуализации')
        self.info_label.setStyleSheet("font-style: italic; color: #666;")
        info_layout.addWidget(self.info_label)
        
        info_panel.setLayout(info_layout)
        main_layout.addWidget(info_panel)
        
        # Инициализация параметров графика
        self.update_chart_options()
        
        # Загружаем данных
        self.load_data()
        
    def update_chart_options(self):
        # Очищаем layout параметров
        for i in reversed(range(self.params_layout.count())): 
            widget = self.params_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        chart_type = self.chart_type_combo.currentText()
        
        if chart_type == 'Гистограмма':
            self.params_layout.addWidget(QLabel('Выберите столбец:'))
            self.column_combo = QComboBox()
            if self.data is not None:
                self.column_combo.addItems(self.data.columns.tolist())
            self.params_layout.addWidget(self.column_combo)
            
            self.params_layout.addWidget(QLabel('Количество бинов:'))
            self.bins_spin = QSpinBox()
            self.bins_spin.setRange(5, 100)
            self.bins_spin.setValue(20)
            self.params_layout.addWidget(self.bins_spin)
            
            plot_btn = QPushButton('Построить гистограмму')
            plot_btn.clicked.connect(self.plot_histogram)
            self.params_layout.addWidget(plot_btn)
            
        elif chart_type == 'Диаграмма рассеяния':
            self.params_layout.addWidget(QLabel('Ось X:'))
            self.x_combo = QComboBox()
            self.params_layout.addWidget(QLabel('Ось Y:'))
            self.y_combo = QComboBox()
            
            if self.data is not None:
                self.x_combo.addItems(self.data.columns.tolist())
                self.y_combo.addItems(self.data.columns.tolist())
                if len(self.data.columns) >= 2:
                    self.x_combo.setCurrentIndex(0)
                    self.y_combo.setCurrentIndex(1)
            
            self.params_layout.addWidget(self.x_combo)
            self.params_layout.addWidget(self.y_combo)
            
            plot_btn = QPushButton('Построить диаграмму рассеяния')
            plot_btn.clicked.connect(self.plot_scatter)
            self.params_layout.addWidget(plot_btn)
            
        elif chart_type == 'Boxplot':
            self.params_layout.addWidget(QLabel('Выберите столбец:'))
            self.box_column_combo = QComboBox()
            if self.data is not None:
                self.box_column_combo.addItems(self.data.columns.tolist())
            self.params_layout.addWidget(self.box_column_combo)
            
            plot_btn = QPushButton('Построить Boxplot')
            plot_btn.clicked.connect(self.plot_boxplot)
            self.params_layout.addWidget(plot_btn)
        
        self.params_layout.addStretch()
        
    def load_data(self):
        try:
            file_name = 'data/client_data_apdated.csv'
            df_0 = pd.read_csv(file_name)
            data_clusters = pd.read_csv('data/client_data_clusters.csv')
            self.data = pd.concat([df_0, data_clusters], axis=1)
            self.canvas.data = self.data
            self.update_data_stats()
            self.update_chart_options()
            self.info_label.setText(f'Данные загружены из файла: {file_name}')
            QMessageBox.information(self, 'Успех', f'Данные успешно загружены!\nЗаписей: {len(self.data)}')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {str(e)}')
            
    def update_data_stats(self):
        if self.data is not None:
            stats_text = (f'Записей: {len(self.data)} | '
                         f'Столбцов: {len(self.data.columns)} | '
                         f'Память: {self.data.memory_usage(deep=True).sum() / 1024:.1f} KB')
            self.stats_label.setText(stats_text)
            
            # Вывод основных статистик в консоль
            #print("\nОсновные статистики данных:")
            #print(self.data.describe())
    
    def plot_histogram(self):
        if self.data is not None:
            column = self.column_combo.currentText()
            bins = self.bins_spin.value()
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            # plot data
            ax.hist(self.data[column], bins, color='skyblue', edgecolor='black')
            ax.set_xlabel(bins)
            ax.set_ylabel(column)
            # refresh canvas
            self.canvas.draw()
            self.info_label.setText(f'Построена гистограмма для столбца "{column}" с {bins} бинами')
            
    def plot_scatter(self):
        if self.data is not None:
            x_column = self.x_combo.currentText()
            y_column = self.y_combo.currentText()
            self.figure.clear()
            # plot data
            ax = self.figure.add_subplot(111)
            ax.scatter(self.data[x_column], self.data[y_column])
            ax.set_xlabel(x_column)
            ax.set_ylabel(y_column)
            # refresh canvas
            self.canvas.draw()
            self.info_label.setText(f'Построена диаграмма рассеяния: {x_column} vs {y_column}')
            
    def plot_boxplot(self):
        if self.data is not None:
            column = self.box_column_combo.currentText()
            self.figure.clear()
            # plot data
            ax = self.figure.add_subplot(111)
            ax.boxplot(self.data[column])
            ax.set_xlabel("Группы данных")
            ax.set_ylabel("Значения")

            # refresh canvas
            self.canvas.draw()
            self.info_label.setText(f'Построен Boxplot для столбца "{column}"')
            
data_analyzer = DataAnalyzer