import pytest
from unittest.mock import MagicMock, patch
from app.controller.noise_controller import NoiseController


class TestNoiseController:

    @patch("app.controller.noise_controller.InfluxDBHandler")
    def test_procesar_lectura_actualiza_stats(self, mock_db_class):
        mock_db_class.return_value.guardar_lectura.return_value = True
        controller = NoiseController()

        payload = {
            "sensor_id": "sensor_01",
            "ubicacion": "Aula_101",
            "decibeles": 65.0
        }
        controller.procesar_lectura(payload)

        assert controller.stats["total"] == 1
        assert controller.stats["suma"] == 65.0

    @patch("app.controller.noise_controller.InfluxDBHandler")
    def test_procesar_lectura_peligrosa_incrementa_alertas(self, mock_db_class):
        mock_db_class.return_value.guardar_lectura.return_value = True
        controller = NoiseController()

        payload = {
            "sensor_id": "sensor_01",
            "ubicacion": "Cafeteria",
            "decibeles": 95.0
        }
        controller.procesar_lectura(payload)

        assert controller.stats["alertas"] == 1

    @patch("app.controller.noise_controller.InfluxDBHandler")
    def test_multiples_lecturas_calcula_maximo(self, mock_db_class):
        mock_db_class.return_value.guardar_lectura.return_value = True
        controller = NoiseController()

        for db in [45.0, 72.0, 88.0, 60.0]:
            controller.procesar_lectura({
                "sensor_id": "s01",
                "ubicacion": "Test",
                "decibeles": db
            })
        assert controller.stats["maximo"] == 88.0
        assert controller.stats["minimo"] == 45.0
        assert controller.stats["total"] == 4