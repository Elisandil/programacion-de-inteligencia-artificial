"""
Controlador de lógica de negocio para el ruido.
Procesa las lecturas recibidas, las almacena en la base de datos y mantiene estadísticas en memoria.
"""

from datetime import datetime
from app.model.noise_data import NoiseData
from app.model.database import InfluxDBHandler
from app.view.console_view import ConsoleView


class NoiseController:
    """
    Controlador principal que implementa la lógica de negocio.
    Recibe datos del MQTTController, los procesa mediante el Model y actualiza la View.
    """

    def __init__(self):
        """Inicializa el controlador con la base de datos y la vista."""
        self.db = InfluxDBHandler()
        self.view = ConsoleView()

        self.stats = {
            "total": 0,
            "suma": 0.0,
            "maximo": float("-inf"),
            "minimo": float("inf"),
            "alertas": 0
        }

    def procesar_lectura(self, payload: dict):
        """
        Procesa una lectura de ruido recibida por MQTT.
        """
        lectura = NoiseData(
            sensor_id=payload.get("sensor_id", "desconocido"),
            ubicacion=payload.get("ubicacion", "desconocida"),
            decibeles=float(payload.get("decibeles", 0)),
            timestamp=datetime.now()
        )
        self._actualizar_stats(lectura)
        guardado = self.db.guardar_lectura(lectura)
        self.view.mostrar_lectura(lectura.to_dict())
        if guardado:
            self.view.mostrar_guardado_ok()

        if self.stats["total"] % 10 == 0:
            self.view.mostrar_estadisticas(self._calcular_stats())

    def _actualizar_stats(self, lectura: NoiseData):
        """Actualiza las estadísticas en memoria con una nueva lectura."""
        self.stats["total"] += 1
        self.stats["suma"] += lectura.decibeles
        self.stats["maximo"] = max(self.stats["maximo"], lectura.decibeles)
        self.stats["minimo"] = min(self.stats["minimo"], lectura.decibeles)
        if lectura.nivel == "peligroso":
            self.stats["alertas"] += 1

    def _calcular_stats(self) -> dict:
        """Calcula las estadísticas actuales para mostrar en la vista."""
        total = self.stats["total"]
        return {
            "total": total,
            "promedio": self.stats["suma"] / total if total > 0 else 0,
            "maximo": self.stats["maximo"] if total > 0 else 0,
            "minimo": self.stats["minimo"] if total > 0 else 0,
            "alertas": self.stats["alertas"]
        }

    def cerrar(self):
        self.db.cerrar()