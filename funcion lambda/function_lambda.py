import json
import pandas as pd
import time
import requests
import random
import time
from datetime import datetime
import datetime
import os
import boto3 #permite conectrase con los buckets

s3_cliente = boto3.client('s3')

def get_estadisticas(api_key, canal_id):
    
    url_canal_estadisticas = 'https://youtube.googleapis.com/youtube/v3/channels?part=statistics&id='+canal_id+'&key='+api_key
    estadisticas_canal = requests.get(url_canal_estadisticas)
    estadisticas_canal = json.loads(estadisticas_canal.content)
    estadisticas_canal=estadisticas_canal['items'][0]['statistics']
    date = pd.to_datetime('today').strftime('%Y-%m-%d')
    datos_canal = {
    'Create_at':date,
    'Total_Vistas':int(float(estadisticas_canal['viewCount'])),
    'Suscripciones':int(float(estadisticas_canal['subscriberCount'])),
    'Cantidad_Videos':int(float(estadisticas_canal['videoCount']))
    }
    
    return datos_canal
    

def canal_estadisticas(df,api_key):
    
    fecha = []
    vistas = []
    suscripciones = []
    cantidad_videos = []
    nombre_canal = []
    
    tiempo = [1,2.5,3,2]
    
    # Iterar el DF
    for i in range(len(df)):
        
        stats_temp = get_estadisticas(api_key,df['Id_Canal'][i])
        nombre_canal.append(df['Nombre_Canal'][i])
        fecha.append(stats_temp['Create_at'])
        vistas.append(stats_temp['Total_Vistas'])
        suscripciones.append(stats_temp['Suscripciones'])
        cantidad_videos.append(stats_temp['Cantidad_Videos'])
        
        
        time.sleep(random.choice(tiempo))
    
    datos = {
        
        'Nombre_Canal':nombre_canal,
        'Suscripciones':suscripciones,
        'Cantidad_Videos':cantidad_videos,
        'Total_Vistas':vistas,
        'created_at':fecha,
        
    }
    
    df_canales_final = pd.DataFrame(datos)
    
    return df_canales_final     


def lambda_handler(event, context):
    
    bucket_name = os.environ['BUCKET_INPUT']
    filename = os.environ['FILE_CHANNEL']
    developer_key = os.environ['API_KEY']
    
    # Obtener el archivo del bucket input
    objeto = s3_cliente.get_object(Bucket=bucket_name, Key=filename)
    df_canales = pd.read_csv(objeto['Body'])
    
    resultados=canal_estadisticas(df_canales,developer_key)
    fecha = pd.to_datetime('today').strftime('%Y%m%d')
    
    resultados.to_csv(f'/tmp/estadisticas_yt_{fecha}.csv', index=False)
    
    # Enviar a bucket destino
    s3 = boto3.resource("s3")
    s3.Bucket(os.environ['BUCKET_OUTPUT']).upload_file(f'/tmp/estadisticas_yt_{fecha}.csv', Key=f'estadisticas_yt_{fecha}.csv')
    
    # Eliminar archivo
    os.remove(f'/tmp/estadisticas_yt_{fecha}.csv')
    
    return f'/tmp/estadisticas_yt_{fecha}.csv ===> Correcto'