# 1. Importación de bibliotecas

import uvicorn
from fastapi import FastAPI
from model import IrisModel, IrisSpecies

# 2. Crear la aplicación y los objetos del modelo

app = FastAPI()
model = IrisModel()

# 3. Exponer la funcionalidad de predicción, realizar una predicción a partir de los datos JSON pasados
#    y devolver la especie de flor predicha con la 

@app.get("/")
def home():
    return {
        "message": "Welcome to the Iris Prediction App!"
    }

@app.post('/predict')
def predict_species(iris: IrisSpecies):
    data = iris.dict()
    prediction, prediction_proba = model.predict_species(data['sepal_length'], data['sepal_width'], data['petal_length'], data['petal_width'])
    return {
        'prediction': prediction,
        'probability': prediction_proba        

    }

# 4. Ejecutar la API con uvicorn
#    Se ejecutará en http://127.0.0.1:8000

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)