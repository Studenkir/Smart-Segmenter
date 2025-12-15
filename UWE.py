import sys
import pandas as pd
import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#import seaborn as sns

# Создадим тестовый датасет, если файл не существует
def create_sample_dataset():
    np.random.seed(42)
    n = 500
    
    data = {
        'age': np.random.randint(18, 70, n),
        'experience': np.random.randint(0, 50, n),
        'income': np.random.normal(50000, 20000, n).clip(10000, 150000),
        'family': np.random.randint(1, 6, n),
        'education': np.random.randint(1, 6, n),  # 1-базовое, 5-высшее
        'mortgage': np.random.normal(200000, 100000, n).clip(0, 500000)
    }
    
    df = pd.DataFrame(data)
    df.to_csv('bank_clients.csv', index=False)
    return df

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        self.data = None
        
    def plot_histogram(self, column, bins=20):
        self.ax.clear()
        if self.data is not None and column in self.data.columns:
            self.ax.hist(self.data[column].dropna(), bins=bins, edgecolor='black', alpha=0.7)
            self.ax.set_title(f'Распределение {column}', fontsize=14)
            self.ax.set_xlabel(column, fontsize=12)
            self.ax.set_ylabel('Частота', fontsize=12)
            self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.draw()
        
    def plot_scatter(self, x_column, y_column):
        self.ax.clear()
        if self.data is not None and x_column in self.data.columns and y_column in self.data.columns:
            self.ax.scatter(self.data[x_column], self.data[y_column], alpha=0.6, edgecolors='w', s=50)
            self.ax.set_title(f'{x_column} vs {y_column}', fontsize=14)
            self.ax.set_xlabel(x_column, fontsize=12)
            self.ax.set_ylabel(y_column, fontsize=12)
            
            # Добавим линию тренда
            z = np.polyfit(self.data[x_column], self.data[y_column], 1)
            p = np.poly1d(z)
            self.ax.plot(self.data[x_column], p(self.data[x_column]), "r--", alpha=0.8)
            
            # Выведем коэффициент корреляции
            corr = self.data[x_column].corr(self.data[y_column])
            self.ax.text(0.05, 0.95, f'Corr: {corr:.3f}', transform=self.ax.transAxes,
                        fontsize=12, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.draw()
        
    def plot_boxplot(self, column):
        self.ax.clear()
        if self.data is not None and column in self.data.columns:
            self.ax.boxplot(self.data[column].dropna())
            self.ax.set_title(f'Boxplot для {column}', fontsize=14)
            self.ax.set_ylabel(column, fontsize=12)
            self.ax.grid(True, alpha=0.3)
            
            # Добавим статистику
            stats = self.data[column].describe()
            stats_text = f"Медиана: {stats['50%']:.2f}\nQ1: {stats['25%']:.2f}\nQ3: {stats['75%']:.2f}"
            self.ax.text(0.05, 0.95, stats_text, transform=self.ax.transAxes,
                        fontsize=10, verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        self.fig.tight_layout()
        self.draw()
        
    def plot_heatmap(self):
        self.ax.clear()
        if self.data is not None:
            # Вычисляем корреляционную матрицу
            corr_matrix = self.data.corr()
            
            # Создаем heatmap
            im = self.ax.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
            
            # Добавляем подписи
            self.ax.set_xticks(np.arange(len(corr_matrix.columns)))
            self.ax.set_yticks(np.arange(len(corr_matrix.columns)))
            self.ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
            self.ax.set_yticklabels(corr_matrix.columns)
            
            # Добавляем значения корреляции в ячейки
            for i in range(len(corr_matrix.columns)):
                for j in range(len(corr_matrix.columns)):
                    text = self.ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                      ha="center", va="center", color="black")
            
            self.ax.set_title('Корреляционная матрица', fontsize=14)
            self.fig.colorbar(im, ax=self.ax)
        self.fig.tight_layout()
        self.draw()

class BankDataAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Анализатор данных банковских клиентов')
        self.setGeometry(100, 100, 1400, 800)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        main_layout = QVBoxLayout(central_widget)
        
        # Панель управления
        control_panel = QGroupBox("Управление данными")
        control_layout = QHBoxLayout()
        
        # Кнопки загрузки данных
        self.load_btn = QPushButton('Загрузить данные из CSV')
        self.load_btn.clicked.connect(self.load_data)
        control_layout.addWidget(self.load_btn)
        
        self.create_sample_btn = QPushButton('Создать пример данных')
        self.create_sample_btn.clicked.connect(self.create_sample_data)
        control_layout.addWidget(self.create_sample_btn)
        
        # Статистика данных
        self.stats_label = QLabel('Данные не загружены')
        control_layout.addWidget(self.stats_label)
        
        control_layout.addStretch()
        control_panel.setLayout(control_layout)
        main_layout.addWidget(control_panel)
        
        # Панель визуализации
        viz_panel = QGroupBox("Визуализация данных")
        viz_layout = QVBoxLayout()
        
        # Выбор типа графика
        chart_type_layout = QHBoxLayout()
        chart_type_layout.addWidget(QLabel('Тип графика:'))
        
        self.chart_type_combo = QComboBox()
        self.chart_type_combo.addItems(['Гистограмма', 'Диаграмма рассеяния', 'Boxplot', 'Тепловая карта корреляций'])
        self.chart_type_combo.currentIndexChanged.connect(self.update_chart_options)
        chart_type_layout.addWidget(self.chart_type_combo)
        
        chart_type_layout.addStretch()
        viz_layout.addLayout(chart_type_layout)
        
        # Панель параметров графика
        self.params_panel = QWidget()
        self.params_layout = QHBoxLayout(self.params_panel)
        viz_layout.addWidget(self.params_panel)
        
        # Виджет для matplotlib
        self.canvas = MatplotlibCanvas(self, width=10, height=6)
        viz_layout.addWidget(self.canvas)
        
        # Добавляем панель инструментов matplotlib
        self.toolbar = NavigationToolbar(self.canvas, self)
        viz_layout.addWidget(self.toolbar)
        
        viz_panel.setLayout(viz_layout)
        main_layout.addWidget(viz_panel)
        
        # Информационная панель
        info_panel = QGroupBox("Информация")
        info_layout = QHBoxLayout()
        
        self.info_label = QLabel('Выберите тип графика и параметры для визуализации')
        self.info_label.setStyleSheet("font-style: italic; color: #666;")
        info_layout.addWidget(self.info_label)
        
        info_panel.setLayout(info_layout)
        main_layout.addWidget(info_panel)
        
        # Инициализация параметров графика
        self.update_chart_options()
        
        # Создаем пример данных при запуске
        self.create_sample_data()
        
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
            
        elif chart_type == 'Тепловая карта корреляций':
            plot_btn = QPushButton('Построить тепловую карту')
            plot_btn.clicked.connect(self.plot_heatmap)
            self.params_layout.addWidget(plot_btn)
        
        self.params_layout.addStretch()
        
    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Загрузить CSV файл', '', 'CSV Files (*.csv)')
        if file_name:
            try:
                self.data = pd.read_csv(file_name)
                self.canvas.data = self.data
                self.update_data_stats()
                self.update_chart_options()
                self.info_label.setText(f'Данные загружены из файла: {file_name}')
                QMessageBox.information(self, 'Успех', f'Данные успешно загружены!\nЗаписей: {len(self.data)}')
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {str(e)}')
                
    def create_sample_data(self):
        try:
            self.data = create_sample_dataset()
            self.canvas.data = self.data
            self.update_data_stats()
            self.update_chart_options()
            self.info_label.setText('Создан пример данных банковских клиентов')
            QMessageBox.information(self, 'Успех', 
                                  f'Пример данных создан успешно!\n'
                                  f'Файл сохранен как: bank_clients.csv\n'
                                  f'Записей: {len(self.data)}')
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось создать данные: {str(e)}')
            
    def update_data_stats(self):
        if self.data is not None:
            stats_text = (f'Записей: {len(self.data)} | '
                         f'Столбцов: {len(self.data.columns)} | '
                         f'Память: {self.data.memory_usage(deep=True).sum() / 1024:.1f} KB')
            self.stats_label.setText(stats_text)
            
            # Вывод основных статистик в консоль
            print("\nОсновные статистики данных:")
            print(self.data.describe())
            
    def plot_histogram(self):
        if self.data is not None:
            column = self.column_combo.currentText()
            bins = self.bins_spin.value()
            self.canvas.plot_histogram(column, bins)
            self.info_label.setText(f'Построена гистограмма для столбца "{column}" с {bins} бинами')
            
    def plot_scatter(self):
        if self.data is not None:
            x_column = self.x_combo.currentText()
            y_column = self.y_combo.currentText()
            self.canvas.plot_scatter(x_column, y_column)
            self.info_label.setText(f'Построена диаграмма рассеяния: {x_column} vs {y_column}')
            
    def plot_boxplot(self):
        if self.data is not None:
            column = self.box_column_combo.currentText()
            self.canvas.plot_boxplot(column)
            self.info_label.setText(f'Построен Boxplot для столбца "{column}"')
            
    def plot_heatmap(self):
        if self.data is not None:
            self.canvas.plot_heatmap()
            self.info_label.setText('Построена тепловая карта корреляций между переменными')

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Установка современного стиля
    
    # Устанавливаем стиль для темной темы
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    
    analyzer = BankDataAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()