import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QComboBox,
                             QTextEdit, QProgressBar, QTabWidget, QGroupBox,
                             QDoubleSpinBox, QTableWidget, QTableWidgetItem, 
                             QHeaderView, QFileDialog, QMessageBox)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QPalette, QColor


class ModelTrainingThread(QThread):
    """Поток для обучения ML-модели"""
    training_progress = pyqtSignal(int)
    training_log = pyqtSignal(str)
    training_finished = pyqtSignal(dict)

    def __init__(self, dataset, test_size=0.2):
        super().__init__()
        self.dataset = dataset
        self.test_size = test_size
        self.model = None

    def run(self):
        try:
            self.training_log.emit("🔄 Начинаем обучение модели...")

            # Подготовка данных
            X_train, X_test, y_train, y_test = train_test_split(
                self.dataset['data'], self.dataset['target'],
                test_size=self.test_size, random_state=42
            )

            # Создание и обучение модели
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)

            self.training_log.emit("📊 Обучение модели...")

            # Имитация прогресса обучения
            for i in range(101):
                self.training_progress.emit(i)
                self.msleep(30)

            self.model.fit(X_train, y_train)

            # Предсказания и метрики
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Расчет precision и recall для многоклассовой классификации
            precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
            
            cm = confusion_matrix(y_test, y_pred)

            # Сбор результатов
            results = {
                'model': self.model,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'confusion_matrix': cm,
                'feature_names': self.dataset['feature_names'],
                'target_names': self.dataset['target_names'],
                'X_test': X_test,
                'y_test': y_test,
                'y_pred': y_pred
            }

            self.training_log.emit(f"✅ Обучение завершено!")
            self.training_log.emit(f"📊 Точность (Accuracy): {accuracy:.3f}")
            self.training_log.emit(f"🎯 Precision: {precision:.3f}")
            self.training_log.emit(f"📈 Recall: {recall:.3f}")
            
            self.training_finished.emit(results)

        except Exception as e:
            self.training_log.emit(f"❌ Ошибка: {str(e)}")


class SimplifiedAIApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.current_dataset = None
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("Упрощенный ML Дашборд")
        self.setGeometry(100, 100, 1200, 800)

        # Центральный виджет с вкладками
        central_widget = QTabWidget()
        self.setCentralWidget(central_widget)

        # Создание вкладок
        central_widget.addTab(self.create_training_tab(), "🎯 Обучение модели")
        central_widget.addTab(self.create_analysis_tab(), "📊 Визуализация данных")

        self.apply_dark_theme()

    def create_training_tab(self):
        """Вкладка обучения модели"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Панель управления
        control_group = QGroupBox("Управление обучением")
        control_layout = QHBoxLayout()

        # Выбор модели
        control_layout.addWidget(QLabel("Модель:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["Random Forest", "SVM", "Neural Network"])
        control_layout.addWidget(self.model_combo)

        # Кнопка загрузки данных
        self.load_btn = QPushButton("📁 Загрузить CSV")
        self.load_btn.clicked.connect(self.load_csv_data)
        control_layout.addWidget(self.load_btn)

        # Выбор целевой переменной
        control_layout.addWidget(QLabel("Целевая переменная:"))
        self.target_combo = QComboBox()
        self.target_combo.setEnabled(False)
        control_layout.addWidget(self.target_combo)

        # Кнопки управления
        self.train_btn = QPushButton("🎓 Обучить модель")
        self.train_btn.clicked.connect(self.start_training)
        self.train_btn.setEnabled(False)
        control_layout.addWidget(self.train_btn)

        control_group.setLayout(control_layout)
        layout.addWidget(control_group)

        # Информация о данных
        self.data_info = QLabel("Данные не загружены")
        self.data_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.data_info)

        # Прогресс-бар
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        # Лог обучения
        self.training_log = QTextEdit()
        self.training_log.setMaximumHeight(200)
        self.training_log.setPlaceholderText("Лог обучения будет отображаться здесь...")
        layout.addWidget(self.training_log)

        # Визуализация результатов
        results_splitter = QHBoxLayout()
        
        # Матрица ошибок
        cm_group = QGroupBox("Матрица ошибок")
        cm_layout = QVBoxLayout()
        self.cm_plot = FigureCanvas(Figure(figsize=(5, 4)))
        cm_layout.addWidget(self.cm_plot)
        cm_group.setLayout(cm_layout)
        results_splitter.addWidget(cm_group)

        # Метрики модели
        metrics_group = QGroupBox("Метрики модели")
        metrics_layout = QVBoxLayout()
        self.metrics_text = QTextEdit()
        self.metrics_text.setPlaceholderText("Метрики модели будут отображаться здесь...")
        metrics_layout.addWidget(self.metrics_text)
        metrics_group.setLayout(metrics_layout)
        results_splitter.addWidget(metrics_group)

        layout.addLayout(results_splitter)
        tab.setLayout(layout)
        return tab

    def create_analysis_tab(self):
        """Вкладка визуализации данных"""
        tab = QWidget()
        layout = QVBoxLayout()

        # Визуализация данных
        plot_group = QGroupBox("Визуализация данных")
        plot_layout = QVBoxLayout()

        # Выбор типа графика
        plot_control_layout = QHBoxLayout()
        plot_control_layout.addWidget(QLabel("Тип графика:"))
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(["Scatter Plot", "Histogram", "Box Plot"])
        self.plot_type_combo.currentTextChanged.connect(self.update_data_visualization)
        plot_control_layout.addWidget(self.plot_type_combo)
        
        plot_control_layout.addWidget(QLabel("Ось X:"))
        self.x_axis_combo = QComboBox()
        self.x_axis_combo.currentTextChanged.connect(self.update_data_visualization)
        plot_control_layout.addWidget(self.x_axis_combo)
        
        plot_control_layout.addWidget(QLabel("Ось Y:"))
        self.y_axis_combo = QComboBox()
        self.y_axis_combo.currentTextChanged.connect(self.update_data_visualization)
        plot_control_layout.addWidget(self.y_axis_combo)
        
        plot_control_layout.addStretch()
        plot_layout.addLayout(plot_control_layout)

        self.data_plot = FigureCanvas(Figure(figsize=(10, 6)))
        plot_layout.addWidget(self.data_plot)

        plot_group.setLayout(plot_layout)
        layout.addWidget(plot_group)

        # Статистика данных
        stats_group = QGroupBox("Статистика данных")
        stats_layout = QVBoxLayout()

        self.data_table = QTableWidget()
        stats_layout.addWidget(self.data_table)

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        tab.setLayout(layout)
        return tab

    def apply_dark_theme(self):
        """Применение темной темы"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
        dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(142, 45, 197).lighter())
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.black)

        self.setPalette(dark_palette)

    def load_csv_data(self):
        """Загрузка CSV-файла с данными"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите CSV файл", "", "CSV Files (*.csv)"
            )
            
            if file_path:
                # Чтение CSV файла
                df = pd.read_csv(file_path)
                
                if df.empty:
                    QMessageBox.warning(self, "Ошибка", "CSV файл пуст!")
                    return
                
                # Обновление комбобоксов для выбора столбцов
                self.target_combo.clear()
                self.target_combo.addItems(df.columns.tolist())
                self.target_combo.setEnabled(True)
                
                self.x_axis_combo.clear()
                self.x_axis_combo.addItems(df.columns.tolist())
                self.y_axis_combo.clear()
                self.y_axis_combo.addItems(df.columns.tolist())
                
                # Сохранение данных
                self.current_dataframe = df
                self.train_btn.setEnabled(True)
                self.data_info.setText(f"Загружено данных: {len(df)} строк, {len(df.columns)} столбцов")
                
                # Обновление визуализации
                self.update_data_visualization()
                self.update_data_stats()
                
                self.training_log.append(f"✅ Загружен файл: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {str(e)}")

    def prepare_dataset(self):
        """Подготовка датасета для обучения"""
        if not hasattr(self, 'current_dataframe'):
            return None
            
        target_column = self.target_combo.currentText()
        
        # Разделение на признаки и целевую переменную
        X = self.current_dataframe.drop(columns=[target_column])
        y = self.current_dataframe[target_column]
        
        # Кодирование категориальных признаков и целевой переменной
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        
        # Кодирование категориальных признаков
        X_encoded = pd.get_dummies(X)
        
        dataset = {
            'data': X_encoded.values,
            'target': y_encoded,
            'feature_names': X_encoded.columns.tolist(),
            'target_names': le.classes_.tolist()
        }
        
        return dataset

    def start_training(self):
        """Запуск обучения модели"""
        dataset = self.prepare_dataset()
        if dataset is None:
            return
            
        self.train_btn.setEnabled(False)
        self.training_log.clear()

        # Запуск потока обучения
        self.training_thread = ModelTrainingThread(dataset)
        self.training_thread.training_progress.connect(self.progress_bar.setValue)
        self.training_thread.training_log.connect(self.update_training_log)
        self.training_thread.training_finished.connect(self.on_training_finished)
        self.training_thread.start()

    def stop_training(self):
        """Остановка обучения"""
        if hasattr(self, 'training_thread') and self.training_thread.isRunning():
            self.training_thread.terminate()
            self.training_thread.wait()
            self.update_training_log("⏹️ Обучение остановлено пользователем")

        self.train_btn.setEnabled(True)

    def update_training_log(self, message):
        """Обновление лога обучения"""
        self.training_log.append(f"{message}")

    def on_training_finished(self, results):
        """Обработка завершения обучения"""
        self.model = results['model']
        self.train_btn.setEnabled(True)

        # Обновление матрицы ошибок
        self.update_confusion_matrix(results)
        
        # Обновление метрик
        self.update_metrics(results)

    def update_confusion_matrix(self, results):
        """Обновление матрицы ошибок"""
        fig = self.cm_plot.figure
        fig.clear()

        ax = fig.add_subplot(111)
        cm = results['confusion_matrix']
        
        im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax.figure.colorbar(im, ax=ax)
        
        # Отображение значений в ячейках
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], 'd'),
                       ha="center", va="center",
                       color="white" if cm[i, j] > cm.max() / 2. else "black")
        
        ax.set_xlabel('Предсказанный класс')
        ax.set_ylabel('Истинный класс')
        ax.set_title('Матрица ошибок')
        ax.set_xticks(range(len(results['target_names'])))
        ax.set_yticks(range(len(results['target_names'])))
        ax.set_xticklabels(results['target_names'])
        ax.set_yticklabels(results['target_names'])

        self.cm_plot.draw()

    def update_metrics(self, results):
        """Обновление метрик модели"""
        metrics_text = f"""
        📊 МЕТРИКИ МОДЕЛИ:

        🔢 Модель: {self.model_combo.currentText()}
        🎯 Accuracy (Точность): {results['accuracy']:.3f}
        🎯 Precision: {results['precision']:.3f}
        📈 Recall: {results['recall']:.3f}

        📋 Матрица ошибок:
        {results['confusion_matrix']}

        🔢 Классификация:
        • Количество классов: {len(results['target_names'])}
        • Количество признаков: {len(results['feature_names'])}
        • Размер тестовой выборки: {len(results['X_test'])}
        """

        self.metrics_text.setText(metrics_text)

    def update_data_visualization(self):
        """Обновление визуализации данных"""
        if not hasattr(self, 'current_dataframe') or self.current_dataframe.empty:
            return

        fig = self.data_plot.figure
        fig.clear()

        plot_type = self.plot_type_combo.currentText()
        x_col = self.x_axis_combo.currentText()
        y_col = self.y_axis_combo.currentText()

        if not x_col or not y_col:
            return

        ax = fig.add_subplot(111)

        try:
            if plot_type == "Scatter Plot":
                if self.target_combo.isEnabled():
                    target_col = self.target_combo.currentText()
                    scatter = ax.scatter(self.current_dataframe[x_col], 
                                       self.current_dataframe[y_col], 
                                       c=pd.Categorical(self.current_dataframe[target_col]).codes,
                                       cmap='viridis', alpha=0.7)
                    fig.colorbar(scatter, ax=ax)
                else:
                    ax.scatter(self.current_dataframe[x_col], 
                             self.current_dataframe[y_col], 
                             alpha=0.7)
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                ax.set_title(f'Scatter Plot: {x_col} vs {y_col}')

            elif plot_type == "Histogram":
                self.current_dataframe[x_col].hist(ax=ax, bins=20, alpha=0.7)
                ax.set_xlabel(x_col)
                ax.set_ylabel('Частота')
                ax.set_title(f'Histogram: {x_col}')

            elif plot_type == "Box Plot":
                if self.target_combo.isEnabled():
                    target_col = self.target_combo.currentText()
                    grouped_data = [self.current_dataframe[self.current_dataframe[target_col] == category][y_col] 
                                  for category in self.current_dataframe[target_col].unique()]
                    ax.boxplot(grouped_data, labels=self.current_dataframe[target_col].unique())
                    ax.set_xlabel(target_col)
                    ax.set_ylabel(y_col)
                    ax.set_title(f'Box Plot: {y_col} по {target_col}')
                else:
                    self.current_dataframe[[x_col, y_col]].boxplot(ax=ax)
                    ax.set_title(f'Box Plot: {x_col} и {y_col}')

            ax.grid(True, alpha=0.3)
            fig.tight_layout()
            self.data_plot.draw()

        except Exception as e:
            ax.text(0.5, 0.5, f"Ошибка визуализации:\n{str(e)}", 
                   ha='center', va='center', transform=ax.transAxes)
            self.data_plot.draw()

    def update_data_stats(self):
        """Обновление статистики данных"""
        if not hasattr(self, 'current_dataframe'):
            return

        df = self.current_dataframe

        self.data_table.setRowCount(len(df.columns))
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels(['Столбец', 'Тип', 'Не-NULL', 'Уникальные', 'Пример'])

        for i, col in enumerate(df.columns):
            self.data_table.setItem(i, 0, QTableWidgetItem(str(col)))
            self.data_table.setItem(i, 1, QTableWidgetItem(str(df[col].dtype)))
            self.data_table.setItem(i, 2, QTableWidgetItem(str(df[col].count())))
            self.data_table.setItem(i, 3, QTableWidgetItem(str(df[col].nunique())))
            
            # Пример значения
            sample_val = str(df[col].iloc[0]) if not df.empty else "N/A"
            if len(sample_val) > 20:
                sample_val = sample_val[:20] + "..."
            self.data_table.setItem(i, 4, QTableWidgetItem(sample_val))

        self.data_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = SimplifiedAIApplication()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()