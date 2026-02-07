"""
Carga de las variables de entorno desde el archivo .env
y las expone como constantes para el resto de la aplicación.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuración MQTT ---
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC_SUBSCRIBE = os.getenv("MQTT_TOPIC", "iot/ruido/#")
MQTT_TOPIC_PUBLISH = "iot/ruido/sensor01"

# --- Configuración InfluxDB ---
INFLUXDB_URL = f"http://{os.getenv('INFLUXDB_HOST', 'localhost')}:8086"
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "mi-token-super-secreto-12345")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "iot_proyecto")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "ruido_ambiental")

# --- Umbrales de ruido (en decibelios) ---
UMBRAL_BAJO = 50        
UMBRAL_MODERADO = 70   
UMBRAL_ALTO = 85       
UMBRAL_PELIGROSO = 85  

UBICACIONES = [
    "Aula_101", "Aula_102", "Biblioteca",
    "Cafeteria", "Laboratorio", "Pasillo_Principal"
]