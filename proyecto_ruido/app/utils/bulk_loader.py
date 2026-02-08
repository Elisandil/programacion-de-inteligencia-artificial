"""
Cargador masivo de datos CSV a InfluxDB.
Útil para cargar el dataset ficticio completo en la base de datos para pruebas y visualización en Grafana.
"""

import csv
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from app.config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET


def cargar_csv_a_influxdb(archivo_csv: str = "data/ruido_ficticio.csv"):
    """
    Lee el CSV generado y lo carga en InfluxDB por lotes.
    """
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = client.write_api(write_options=SYNCHRONOUS)

    puntos = []
    with open(archivo_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            point = (
                Point("ruido_ambiental")
                .tag("sensor_id", row["sensor_id"])
                .tag("ubicacion", row["ubicacion"])
                .tag("nivel", row["nivel"])
                .field("decibeles", float(row["decibeles"]))
                .time(
                    datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"),
                    WritePrecision.S
                )
            )
            puntos.append(point)

    # Escribir en lotes de 100
    batch_size = 100
    for i in range(0, len(puntos), batch_size):
        batch = puntos[i:i + batch_size]
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=batch)
        print(f"  Lote {i // batch_size + 1}: {len(batch)} puntos escritos")

    client.close()
    print(f"\nTotal: {len(puntos)} registros cargados en InfluxDB")


if __name__ == "__main__":
    cargar_csv_a_influxdb()