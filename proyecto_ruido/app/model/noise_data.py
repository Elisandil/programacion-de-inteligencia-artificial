"""
Modelo de datos para las lecturas de ruido.
Representa una medición individual del sensor con todos sus atributos.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class NoiseData:
    """
    Clase que representa una lectura del sensor de ruido.
    """
    sensor_id: str
    ubicacion: str
    decibeles: float
    nivel: str = field(init=False)  # Se calcula automáticamente
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Calcula automáticamente el nivel de ruido tras la inicialización."""
        self.nivel = self.clasificar_ruido(self.decibeles)

    @staticmethod
    def clasificar_ruido(db: float) -> str:
        """
        Clasifica el nivel de ruido según los decibelios medidos.
        """
        if db < 50:
            return "bajo"
        elif db < 70:
            return "moderado"
        elif db < 85:
            return "alto"
        else:
            return "peligroso"

    def to_dict(self) -> dict:
        """Convierte la lectura a diccionario para serialización JSON."""
        return {
            "sensor_id": self.sensor_id,
            "ubicacion": self.ubicacion,
            "decibeles": round(self.decibeles, 2),
            "nivel": self.nivel,
            "timestamp": self.timestamp.isoformat()
        }

    def __str__(self) -> str:
        return (f"[{self.timestamp:%H:%M:%S}] {self.sensor_id} @ {self.ubicacion}: "
                f"{self.decibeles:.2f} dB ({self.nivel})")