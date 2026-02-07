"""
Handler de base de datos InfluxDB.
Gestiona la conexión, escritura y consulta de datos de ruido en la base de datos time-series InfluxDB 2.x.
"""

from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from app.config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET
from app.model.noise_data import NoiseData


class InfluxDBHandler:
    """
    Maneja las operaciones CRUD de InfluxDB.
    """

    def __init__(self):
        self.client = InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
        )
        # API de escritura síncrona (espera confirmación)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        # API de consulta (Flux query language)
        self.query_api = self.client.query_api()
        self.bucket = INFLUXDB_BUCKET
        self.org = INFLUXDB_ORG

    def guardar_lectura(self, data: NoiseData) -> bool:
        """
        Guarda una lectura de ruido en InfluxDB.
        """
        try:
            
            point = (
                Point("ruido_ambiental")
                .tag("sensor_id", data.sensor_id)
                .tag("ubicacion", data.ubicacion)
                .tag("nivel", data.nivel)
                .field("decibeles", data.decibeles)
                .time(data.timestamp, WritePrecision.MS)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            return True
        except Exception as e:
            print(f"Error al guardar en InfluxDB: {e}")
            return False

    def obtener_ultimas_lecturas(self, limite: int = 100) -> list:
        """
        Obtiene las últimas N lecturas de ruido.
        """

        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: -24h)
            |> filter(fn: (r) => r._measurement == "ruido_ambiental")
            |> filter(fn: (r) => r._field == "decibeles")
            |> sort(columns: ["_time"], desc: true)
            |> limit(n: {limite})
        '''
        try:
            tables = self.query_api.query(query, org=self.org)
            resultados = []
            for table in tables:
                for record in table.records:
                    resultados.append({
                        "timestamp": record.get_time(),
                        "sensor_id": record.values.get("sensor_id"),
                        "ubicacion": record.values.get("ubicacion"),
                        "nivel": record.values.get("nivel"),
                        "decibeles": record.get_value()
                    })
            return resultados
        except Exception as e:
            print(f"Error al consultar InfluxDB: {e}")
            return []

    def obtener_promedio_por_ubicacion(self) -> list:
        """
        Calcula el promedio de decibelios por ubicación en la última hora.
        """
        query = f'''
        from(bucket: "{self.bucket}")
            |> range(start: -1h)
            |> filter(fn: (r) => r._measurement == "ruido_ambiental")
            |> filter(fn: (r) => r._field == "decibeles")
            |> group(columns: ["ubicacion"])
            |> mean()
        '''
        try:
            tables = self.query_api.query(query, org=self.org)
            resultados = []
            for table in tables:
                for record in table.records:
                    resultados.append({
                        "ubicacion": record.values.get("ubicacion"),
                        "promedio_db": round(record.get_value(), 2)
                    })
            return resultados
        except Exception as e:
            print(f"Error al consultar promedios: {e}")
            return []

    def cerrar(self):
        self.client.close()