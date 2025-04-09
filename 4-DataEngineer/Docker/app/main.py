from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import matplotlib.pyplot as plt

app = FastAPI()


@app.get("/")
async def inicio():
    return {"mensaje":"Hola!!"}

@app.get("/obtener-iris")
def obtener_iris():
    url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    iris = pd.read_csv(url)
    return iris.to_dict(orient='records')

@app.get("/graficar-iris")
def graficar_iris():
    url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    iris = pd.read_csv(url)

    plt.scatter(iris['sepal_length'], iris['sepal_width'])
    plt.savefig('iris.png')
    archivo = open('iris.png', mode="rb")

    return StreamingResponse(archivo, media_type="image/png")
