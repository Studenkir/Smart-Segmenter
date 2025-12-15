from sklearn.decomposition import PCA
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class MLModels:
    def __init__(self):
        self.data = pd.read_csv('data/client_data_apdated.csv')
        self.all_features = []
        #self.continuous_variables = {}
        #self.categorical_variables = {}
        
    def load_str(self, a: str):
        return a + 'ssdd'
    
    def load_dataset(self):
        """Загружаем датасет с данными о клиентах"""
        data = pd.read_csv('data/client_data_apdated.csv')
        return data[0:600]
    
    def scaler_data(self, langs_continuous , langs_categorical):
        """ Масштабирование признаков """
        features_for_clustering = [key for key, value in langs_continuous.items() if value == 1]
        additional_features = [key for key, value in langs_categorical.items() if value == 1]
        data = self.data
        scaler = StandardScaler()
        clust_status = True
        
        if features_for_clustering == [] and additional_features == []:
            self.all_features = ['age']
            clust_status = False
        else:
            self.all_features = features_for_clustering + additional_features
            clust_status = True

        self.scaled_features = scaler.fit_transform(data[self.all_features])
        return clust_status
    
    def for_plot_elbow(self, k_range):
        """ Метод локтя """
        inertia = []
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(self.scaled_features)
            inertia.append(kmeans.inertia_)
        return inertia
    
    def for_plot_cluster_graph(self, optimal_k):
        """ Кластеризация KMeans """
        data = self.data
        kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
        data['cluster_KMeans'] = kmeans.fit_predict(self.scaled_features)
        data['cluster_KMeans'].to_csv('data/client_data_clusters.csv', index=False)

        # Визуализация кластеров (для 2D)
        pca = PCA(n_components=2)
        pca_features = pca.fit_transform(self.scaled_features)
        return pca_features, data
    
    def load_profiles(self, features_list=None) -> tuple[pd.DataFrame, list, dict]:
        """Создание профилей кластеров"""
        
        # Используем переданные признаки или атрибут класса
        features_to_use = features_list if features_list is not None else self.all_features
        
        data_clusters = pd.read_csv('data/client_data_clusters.csv')
        variables_dict_mean = {key: 'mean' for key in features_to_use}
        result = pd.concat([self.data, data_clusters], axis=1)
        
        cluster_summary: pd.DataFrame = result.groupby('cluster_KMeans').agg(variables_dict_mean).round(2)

        # Добавление размера кластера
        cluster_summary['Size'] = result['cluster_KMeans'].value_counts().sort_index()
        cluster_summary['Percentage'] = (cluster_summary['Size'] / len(result) * 100).round(2)
        
        l = ["Молодые клиенты с низким доходом, редко используют кредитные продукты", "Клиенты предпенсионного возраста со стабильным доходом",
        "Состоятельные клиенты среднего возраста, активно пользующиеся кредитами", "Высокорисковые клиенты с просрочками" ]
        
        #clusters_descriptions = {key: 'Описание кластера' for key in range(1, len(features_to_use)+1)}
        clusters_descriptions = {
            0: "Молодые клиенты с низким доходом, редко используют кредитные продукты",
            1: "Клиенты предпенсионного возраста со стабильным доходом",
            2: "Состоятельные клиенты среднего возраста, активно пользующиеся кредитами",
            3: "Высокорисковые клиенты с просрочками"
        }
        
        d = {}
        for cluster_num, description in clusters_descriptions.items():
            if cluster_num in result['cluster_KMeans'].values:
                size = len(result[result['cluster_KMeans'] == cluster_num])
                d[cluster_num] = [f'{description}', size, round(size/len(result)*100, 4)]
        
        return cluster_summary, features_to_use, d
    
# Создаем глобальный экземпляр для использования в приложении
ml_models = MLModels()