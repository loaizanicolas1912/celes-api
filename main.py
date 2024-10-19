from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import numpy as np
import pandas as pd
import joblib
import os
from google.cloud import storage

app = FastAPI()

# Función para descargar el modelo desde GCS
def download_model():
    # Inicializar el cliente de GCS
    client = storage.Client()
    bucket_name = 'model-cluster'
    blob_name = 'xgboost_model_celes.pkl'
    
    # Crear el bucket y el blob
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Descargar el modelo
    local_model_path = 'xgboost_model_celes.pkl'
    blob.download_to_filename(local_model_path)
    return local_model_path

# Descargar el modelo antes de iniciar la aplicación
model_path = download_model()
# Cargar el modelo entrenado
model = joblib.load(model_path)

# Función para transformar las columnas del DataFrame
def transform_preparation(df):
    columns = ['NombreProducto', 'resum_name', 'marca', 'TipoCliente']
    for i in columns:
        df[i] = df[i].astype('category')
    return df

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    # Leer el archivo CSV
    df = pd.read_csv(file.file)
    df_prediction = transform_preparation(df)

    # Hacer predicciones
    predict_values = model.predict(df_prediction)
    df_prediction['predict_demand'] = np.expm1(predict_values)

    # Guardar el DataFrame con predicciones a un archivo CSV
    output_file = 'predicciones.csv'
    df_prediction.to_csv(output_file, index=False)

    # Devolver el archivo CSV como respuesta
    response = FileResponse(output_file, media_type='text/csv', filename='predict_demand.csv')
    return response
