# 1. Importación de bibliotecas
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pydantic import BaseModel
import joblib

# 2. Clase que describe las medidas de una única flor
class IrisSpecies(BaseModel):
    sepal_length: float 
    sepal_width: float 
    petal_length: float 
    petal_width: float

# 3. Clase para entrenar el modelo y hacer predicciones
class IrisModel:
    # Constructor de la clase, carga el conjunto de datos y carga el modelo
    # si existe. Si no, llama al método _train_model y 
    # guarda el modelo
    def __init__(self):
        self.df = pd.read_csv('iris.csv')
        self.model_fname_ = 'iris_model.pkl'
        try:
            self.model = joblib.load(self.model_fname_)
        except Exception as _:
            self.model = self._train_model()
            joblib.dump(self.model, self.model_fname_)

    # 4. Entrena el modelo usando el clasificador RandomForest
    def _train_model(self):
        X = self.df.drop('variety', axis=1)
        y = self.df['variety']
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        return model

    # 5. Realiza una predicción utilizando el modelo entrenado
    def predict_species(self, sepal_length, sepal_width, petal_length, petal_width):
        data_in = [[sepal_length, sepal_width, petal_length, petal_width]]
        prediction_proba = self.model.predict_proba(data_in).tolist()
        prediction = self.model.predict(data_in).tolist()
        return prediction[0], prediction_proba[0]
