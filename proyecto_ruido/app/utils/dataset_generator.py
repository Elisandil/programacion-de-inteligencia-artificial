"""
Generador de dataset ficticio de ruido ambiental.
Crea datos simulados con patrones realistas:
- Mayor ruido en horario laboral (8-18h)
- Variación por ubicación (cafetería más ruidosa que biblioteca)
- Picos aleatorios para simular eventos
"""

import csv
import random
from datetime import datetime, timedelta
from app.config import UBICACIONES
from app.model.noise_data import NoiseData


class DatasetGenerator:
    """
    Genera datos ficticios de ruido para pruebas y demostración.
    Los datos siguen patrones realistas basados en hora del día y tipo de ubicación.
    """

    RUIDO_BASE = {
        "Aula_101": 55,
        "Aula_102": 58,
        "Biblioteca": 35,
        "Cafeteria": 72,
        "Laboratorio": 60,
        "Pasillo_Principal": 65
    }

    @classmethod
    def generar_dataset(cls, num_registros: int = 500,
                        dias: int = 7,
                        archivo_csv: str = "data/ruido_ficticio.csv") -> list:
        """
        Genera un dataset completo de lecturas de ruido ficticias.
        """
        datos = []
        fecha_inicio = datetime.now() - timedelta(days=dias)

        for i in range(num_registros):
            offset = random.uniform(0, dias * 24 * 3600)
            timestamp = fecha_inicio + timedelta(seconds=offset)
            ubicacion = random.choice(UBICACIONES)
            db = cls._calcular_db_realista(ubicacion, timestamp)

            lectura = NoiseData(
                sensor_id=f"sensor_{UBICACIONES.index(ubicacion) + 1:02d}",
                ubicacion=ubicacion,
                decibeles=db,
                timestamp=timestamp
            )
            datos.append(lectura)

        datos.sort(key=lambda x: x.timestamp)
        cls._guardar_csv(datos, archivo_csv)

        return datos

    @classmethod
    def _calcular_db_realista(cls, ubicacion: str, timestamp: datetime) -> float:
        """
        Calcula un valor de decibelios realista basado en la ubicación
        y la hora del día.
        """
        base = cls.RUIDO_BASE.get(ubicacion, 50)
        hora = timestamp.hour

        # Factor horario
        if hora < 6:
            factor = 0.5
        elif hora < 8:
            factor = 0.8
        elif hora < 14:
            factor = 1.2
        elif hora < 16:
            factor = 0.9
        elif hora < 20:
            factor = 1.1
        else:
            factor = 0.7

        variacion = random.gauss(0, base * 0.15)
        db = base * factor + variacion

        if random.random() < 0.05:
            db += random.uniform(15, 35)

        return max(30.0, min(120.0, round(db, 2)))

    @staticmethod
    def _guardar_csv(datos: list, archivo: str):
        """
        Guarda la lista de lecturas en un archivo CSV.
        """
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Cabecera
            writer.writerow([
                "timestamp", "sensor_id", "ubicacion", "decibeles", "nivel"
            ])
            # Datos
            for lectura in datos:
                writer.writerow([
                    lectura.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    lectura.sensor_id,
                    lectura.ubicacion,
                    lectura.decibeles,
                    lectura.nivel
                ])
        print(f"Dataset guardado en: {archivo} ({len(datos)} registros)")