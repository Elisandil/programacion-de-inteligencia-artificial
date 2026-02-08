import pytest
from datetime import datetime
from app.model.noise_data import NoiseData


class TestNoiseData:

    def test_clasificacion_bajo(self):
        lectura = NoiseData("s01", "Biblioteca", 35.0)
        assert lectura.nivel == "bajo"

    def test_clasificacion_moderado(self):
        lectura = NoiseData("s01", "Aula_101", 60.0)
        assert lectura.nivel == "moderado"

    def test_clasificacion_alto(self):
        lectura = NoiseData("s01", "Cafeteria", 78.0)
        assert lectura.nivel == "alto"

    def test_clasificacion_peligroso(self):
        lectura = NoiseData("s01", "Laboratorio", 95.0)
        assert lectura.nivel == "peligroso"

    def test_clasificacion_limite_50(self):
        lectura = NoiseData("s01", "Test", 50.0)
        assert lectura.nivel == "moderado"

    def test_clasificacion_limite_85(self):
        """Exactamente 85 dB debe ser 'peligroso' (>= 85)."""
        lectura = NoiseData("s01", "Test", 85.0)
        assert lectura.nivel == "peligroso"

    def test_to_dict_contiene_campos(self):
        lectura = NoiseData("sensor_01", "Aula_101", 65.5)
        d = lectura.to_dict()
        assert "sensor_id" in d
        assert "ubicacion" in d
        assert "decibeles" in d
        assert "nivel" in d
        assert "timestamp" in d

    def test_to_dict_valores_correctos(self):
        lectura = NoiseData("sensor_02", "Cafeteria", 72.45)
        d = lectura.to_dict()
        assert d["sensor_id"] == "sensor_02"
        assert d["ubicacion"] == "Cafeteria"
        assert d["decibeles"] == 72.45
        assert d["nivel"] == "alto"

    def test_str_format(self):
        lectura = NoiseData("s01", "Biblioteca", 40.0)
        texto = str(lectura)
        assert "s01" in texto
        assert "Biblioteca" in texto
        assert "40.00" in texto
        assert "bajo" in texto

    def test_timestamp_automatico(self):
        lectura = NoiseData("s01", "Test", 50.0)
        assert isinstance(lectura.timestamp, datetime)

    def test_decibeles_redondeo(self):
        lectura = NoiseData("s01", "Test", 65.456789)
        d = lectura.to_dict()
        assert d["decibeles"] == 65.46