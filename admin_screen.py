from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
                             QLabel, QPushButton, QGroupBox, QSpinBox,
                             QGridLayout, QSizePolicy)
from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

from ml_models import MLModels

class AdminScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.langs_continuous = {'age':0, 'experience':0,
                                'income':0, 'family':0, 'mortgage':0}
        self.langs_categorical = {'personal_loan':0, 'creditcard':0, 'loan_delinquency':0,
                                  'non_valid_passport':0, 'undergraduate_edu':0,
                                  'graduate_edu':0, 'advance_edu':0}
        self.min_num_clusters = 2
        self.max_num_clusters = 11
        self.num_clusters = 5
        self.error_style = """
            color: #FF9800; 
            font-weight: bold; 
            padding: 4px;
            background-color: #FFF3E0;
            border-radius: 2px;
        """
        self.green_style = """
            color: #4CAF50; 
            font-weight: bold; 
            padding: 4px;
            background-color: #E8F5E8;
            border-radius: 2px;
        """

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)  # Увеличиваем расстояние между элементами
        layout.setContentsMargins(10, 10, 10, 10)  # Добавляем отступы от краев

        # Заголовок
        title = QLabel("--> Административная панель <--")
        title.setStyleSheet("font-size: 14pt; font-weight: bold; margin: 8px;")
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        layout.addWidget(title)

        """ Окно для подбора параметров и кластеризации """
        
        control_group = QGroupBox("✏️ Параметры кластеризации")
        control_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; 
                margin: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        control_layout = QGridLayout(control_group)
        #control_layout = QHBoxLayout(control_group)
        control_layout.setSpacing(10)  # Расстояние между кнопками
        control_layout.setContentsMargins(15, 20, 15, 15)  # Отступы внутри группы

        """ Кнопка для очистки кэша """
        control_layout.addWidget(QLabel("Выберите непрерывные числовые переменные для кластеризации:"), 0, 0, 1, 5)
        
        """ Чек бокс 1 """
        checkbox_1 = QCheckBox()
        checkbox_1.stateChanged.connect(self.checked_1)
        checkbox_1.setText("Возраст")
        control_layout.addWidget(checkbox_1, 1, 0)
        #checkbox_a.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        """ Чек бокс 2 """
        checkbox_2 = QCheckBox()
        checkbox_2.stateChanged.connect(self.checked_2)
        checkbox_2.setText("Стаж")
        control_layout.addWidget(checkbox_2, 1, 1)
        
        """ Чек бокс 3 """
        checkbox_3 = QCheckBox()
        checkbox_3.stateChanged.connect(self.checked_3)
        checkbox_3.setText("Доход")
        control_layout.addWidget(checkbox_3, 1, 2)
        
        """ Чек бокс 4 """
        checkbox_4 = QCheckBox()
        checkbox_4.stateChanged.connect(self.checked_4)
        checkbox_4.setText("Размер семьи")
        control_layout.addWidget(checkbox_4, 1, 3)

        """ Чек бокс 5 """
        checkbox_5 = QCheckBox()
        checkbox_5.stateChanged.connect(self.checked_5)
        checkbox_5.setText("Ипотека")
        control_layout.addWidget(checkbox_5, 1, 4)
        
        control_layout.addWidget(QLabel("Выберите категориальные переменные для кластеризации:"), 2, 0, 1, 5)
        
        """ Чек бокс 6 """
        checkbox_6 = QCheckBox()
        checkbox_6.stateChanged.connect(self.checked_6)
        checkbox_6.setText("Одобрение заёма")
        control_layout.addWidget(checkbox_6, 3, 0)
        
        """ Чек бокс 7 """
        checkbox_7 = QCheckBox()
        checkbox_7.stateChanged.connect(self.checked_7)
        checkbox_7.setText("Наличие кредкарты")
        control_layout.addWidget(checkbox_7, 3, 1)
        
        """ Чек бокс 8 """
        checkbox_8 = QCheckBox()
        checkbox_8.stateChanged.connect(self.checked_8)
        checkbox_8.setText("Просрочка кредита")
        control_layout.addWidget(checkbox_8, 3, 2)
        
        """ Чек бокс 9 """
        checkbox_9 = QCheckBox()
        checkbox_9.stateChanged.connect(self.checked_9)
        checkbox_9.setText("Просроченный паспорт")
        control_layout.addWidget(checkbox_9, 3, 3)
        
        """ Чек бокс 10 """
        checkbox_10 = QCheckBox()
        checkbox_10.stateChanged.connect(self.checked_10)
        checkbox_10.setText("Образование")
        control_layout.addWidget(checkbox_10, 3, 4)
        
        """ Выбор количества кластеров для метода локтя """
        control_layout.addWidget(QLabel("Кол-во кластеров (min):"), 4, 0)
        cluster_spin_0 = QSpinBox()
        cluster_spin_0.setRange(1, 19)
        cluster_spin_0.setValue(2)
        cluster_spin_0.valueChanged.connect(self.min_value_changed)
        control_layout.addWidget(cluster_spin_0, 4, 1)
        
        """ Выбор количества кластеров для метода локтя """
        control_layout.addWidget(QLabel("Кол-во кластеров (max):"), 4, 2)
        cluster_spin_1 = QSpinBox()
        cluster_spin_1.setRange(2, 20)
        cluster_spin_1.setValue(11)
        cluster_spin_1.valueChanged.connect(self.max_value_changed)
        control_layout.addWidget(cluster_spin_1, 4, 3)

        """ Кнопка для начала метода локтя """
        elbow_btn = QPushButton("📐 Построить elbow график")
        elbow_btn.setStyleSheet("""
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
        elbow_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        elbow_btn.clicked.connect(self.plot_elbow)
        control_layout.addWidget(elbow_btn, 5, 0, 1, 2)
        
        """ Выбор конечного числа кластеров """
        control_layout.addWidget(QLabel("Кол-во кластеров:"), 6, 0)
        cluster_spin_2 = QSpinBox()
        cluster_spin_2.setRange(2, 20)
        cluster_spin_2.setValue(5)
        cluster_spin_2.valueChanged.connect(self.value_segments)
        control_layout.addWidget(cluster_spin_2, 6, 1)
        
        """ Кнопка для начала сегментации """
        segmentation_btn = QPushButton("✂️ Сегментация")
        segmentation_btn.setStyleSheet("""
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
        segmentation_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        segmentation_btn.clicked.connect(self.plot_cluster_graph)
        control_layout.addWidget(segmentation_btn, 6, 2, 1, 2)
        
        """ Пустота """
        control_layout.addWidget(QLabel(" "), 6, 5)
        control_layout.addWidget(QLabel(" "), 6, 6)
        control_layout.addWidget(QLabel(" "), 6, 7)
        control_layout.addWidget(QLabel(" "), 6, 8)
        
        """ График локтя окно """
        # a figure instance to plot on
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        control_layout.addWidget(self.canvas, 0, 6, 6, 4)
        self.toolbar = NavigationToolbar(self.canvas)
        control_layout.addWidget(self.toolbar, 6, 6, 1, 4)

        layout.addWidget(control_group)

        """ Окно с быстрыми действиями ниже """

        # Быстрые действия
        actions_group = QGroupBox("🚀 Быстрые действия")
        actions_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; 
                margin: 5px;
                padding-top: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 5px;
                padding: 0 5px 0 5px;
            }
        """)
        actions_layout = QHBoxLayout(actions_group)
        actions_layout.setSpacing(10)  # Расстояние между кнопками
        actions_layout.setContentsMargins(15, 20, 15, 15)  # Отступы внутри группы

        """ Кнопка для очистки кэша """
        clear_cache_btn = QPushButton("🗑️ Очистить кэш")
        clear_cache_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336; 
                color: white; 
                border: none; 
                padding: 4px; 
                border-radius: 2px;
                min-width: 90px;
            }
            QPushButton:hover {
                background-color: #D32F2F;
            }
        """)
        clear_cache_btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        clear_cache_btn.clicked.connect(self.clear_cache)

        actions_layout.addWidget(clear_cache_btn)
        actions_layout.addStretch()  # Добавляем растягивающееся пространство справа

        layout.addWidget(actions_group)

        """ Вывод статусов системы ниже """

        # Статус системы
        status_group = QGroupBox("🔧 Статус системы")
        status_group.setStyleSheet("""
            QGroupBox { 
                font-weight: bold; 
                margin: 5px;
                padding-top: 5px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 5px;
                padding: 0 5px 0 5px;
            }
        """)
        status_layout = QVBoxLayout(status_group)
        status_layout.setContentsMargins(15, 20, 15, 15)  # Отступы внутри группы

        self.status_label = QLabel("✅ Все системы работают нормально")
        self.status_label.setStyleSheet("""
            color: #4CAF50; 
            font-weight: bold; 
            padding: 4px;
            background-color: #E8F5E8;
            border-radius: 2px;
        """)
        self.status_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.status_label.setMinimumHeight(30)  # Минимальная высота для статуса

        status_layout.addWidget(self.status_label)

        layout.addWidget(status_group)

        layout.addStretch()

        # Загружаем начальные метрики
        #self.refresh_metrics()
    
    def checked_1(self, checked):
        if checked: self.langs_continuous['age']= 1
        else: self.langs_continuous['age']= 0
        self.show()
        
    def checked_2(self, checked):
        if checked: self.langs_continuous['income']= 1
        else: self.langs_continuous['income']= 0
        self.show()
    
    def checked_3(self, checked):
        if checked: self.langs_continuous['income']= 1
        else: self.langs_continuous['income']= 0
        self.show()
        
    def checked_4(self, checked):
        if checked: self.langs_continuous['family']= 1
        else: self.langs_continuous['family']= 0
        self.show()
    
    def checked_5(self, checked):
        if checked: self.langs_continuous['mortgage']= 1
        else: self.langs_continuous['mortgage']= 0
        self.show()
        
    def checked_6(self, checked):
        if checked: self.langs_continuous['personal_loan']= 1
        else: self.langs_continuous['personal_loan']= 0
        self.show()
        
    def checked_7(self, checked):
        if checked: self.langs_continuous['creditcard']= 1
        else: self.langs_continuous['creditcard']= 0
        self.show()
        
    def checked_8(self, checked):
        if checked: self.langs_continuous['loan_delinquency']= 1
        else: self.langs_continuous['loan_delinquency']= 0
        self.show()
        
    def checked_9(self, checked):
        if checked: self.langs_continuous['non_valid_passport']= 1
        else: self.langs_continuous['non_valid_passport']= 0
        self.show()
        
    def checked_10(self, checked):
        if checked:
            self.langs_continuous['undergraduate_edu']= 1
            self.langs_continuous['graduate_edu']= 1
            self.langs_continuous['advance_edu']= 1
        else:
            self.langs_continuous['undergraduate_edu']= 0
            self.langs_continuous['graduate_edu']= 0
            self.langs_continuous['advance_edu']= 0
        self.show()
        
    def min_value_changed(self, i):
        self.min_num_clusters = i
        
    def max_value_changed(self, i):
        self.max_num_clusters = i
        
    def value_segments(self, i):
        self.num_clusters = i
    
    def plot_elbow(self):
        if self.min_num_clusters >= self.max_num_clusters:
            self.plot_elbow_def()
        else:
            k_range = range(self.min_num_clusters, self.max_num_clusters)
            a = MLModels()
            clust_status = a.scaler_data(self.langs_continuous, self.langs_categorical)
            
            if clust_status:
                inertia = a.for_plot_elbow(k_range)
        
                # clearing old figure
                self.figure.clear()
                # create an axis
                ax = self.figure.add_subplot(111)
                # plot data
                ax.plot(k_range, inertia, 'bo-')
                ax.set_xlabel('Number of clusters')
                ax.set_ylabel('Inertia')
                ax.set_title('Elbow Method')
                # refresh canvas
                self.canvas.draw()
                self.on_plot_elbow()
            else:
                self.no_variables_clustering()
            
    def plot_cluster_graph(self):
        a = MLModels()
        clust_status = a.scaler_data(self.langs_continuous, self.langs_categorical)
        
        if clust_status:
            pca_features, df = a.for_plot_cluster_graph(self.num_clusters)
            # clearing old figure
            self.figure.clear()
            # create an axis
            ax = self.figure.add_subplot(111)
            # plot data
            scatter = ax.scatter(pca_features[:, 0], pca_features[:, 1],
                            c=df['cluster_KMeans'], cmap='viridis', alpha=0.6)
            ax.set_xlabel('PCA Component 1')
            ax.set_ylabel('PCA Component 2')
            ax.set_title('Кластеризация клиентов (KMeans)')

            # refresh canvas
            self.canvas.draw()
            self.on_plot_elbow()
            self.on_plot_elbow()
        else:
            self.no_variables_clustering()
    
    def retrain_model(self):
        """Запускает переобучение модели"""
        print("🎯 Запуск переобучения модели...")
        self.status_label.setText("🔄 Модель переобучается...")
        self.status_label.setStyleSheet(self.error_style)

        # Имитация задержки переобучения
        QTimer.singleShot(2000, self.on_retrain_complete)

    def on_retrain_complete(self):
        """Вызывается после завершения переобучения"""
        print("✅ Модель успешно переобучена!")
        self.status_label.setText("✅ Модель актуальна, все системы работают нормально")
        self.status_label.setStyleSheet(self.green_style)

    def clear_cache(self):
        """Очищает кэш системы"""
        print("🗑️ Очистка кэша...")
        self.status_label.setText("🗑️ Очистка кэша...")
        self.status_label.setStyleSheet(self.error_style)

        # Имитация задержки очистки
        QTimer.singleShot(1000, self.on_cache_cleared)

    def on_cache_cleared(self):
        """Вызывается после очистки кэша"""
        print("✅ Кэш успешно очищен!")
        self.status_label.setText("✅ Кэш очищен, все системы работают нормально")
        self.status_label.setStyleSheet(self.green_style)
        
    def plot_elbow_def(self):
        """Указываем на ошибку в plot_elbow"""
        print('min_num_clusters должно быть < max_num_clusters')
        self.status_label.setText("❗ Кол-во класт.(min) должно быть < Кол-во класт.(max)")
        self.status_label.setStyleSheet(self.error_style)
    
    def no_variables_clustering(self):
        """Указываем на ошибку в plot_elbow и check_buffering_conditions"""
        print('Выбрано 0 переменных для кластеризации')
        self.status_label.setText("❗ Выбрано 0 переменных для кластеризации")
        self.status_label.setStyleSheet(self.error_style)

    def on_plot_elbow(self):
        """Вызывается после устранения ошибки в plot_elbow и check_buffering_conditions"""
        self.status_label.setText("✅ График построен. Все системы работают нормально")
        self.status_label.setStyleSheet(self.green_style)