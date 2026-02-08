import os
import pytest
from app.utils.dataset_generator import DatasetGenerator


class TestDatasetGenerator:

    def test_genera_cantidad_correcta(self, tmp_path):
        archivo = str(tmp_path / "test.csv")
        datos = DatasetGenerator.generar_dataset(
            num_registros=50, dias=1, archivo_csv=archivo
        )
        assert len(datos) == 50

    def test_datos_en_rango_valido(self, tmp_path):
        archivo = str(tmp_path / "test.csv")
        datos = DatasetGenerator.generar_dataset(
            num_registros=200, dias=3, archivo_csv=archivo
        )
        for lectura in datos:
            assert 30.0 <= lectura.decibeles <= 120.0

    def test_csv_se_crea(self, tmp_path):
        archivo = str(tmp_path / "test.csv")
        DatasetGenerator.generar_dataset(
            num_registros=10, dias=1, archivo_csv=archivo
        )
        assert os.path.exists(archivo)

    def test_csv_tiene_cabecera(self, tmp_path):
        archivo = str(tmp_path / "test.csv")
        DatasetGenerator.generar_dataset(
            num_registros=5, dias=1, archivo_csv=archivo
        )
        with open(archivo, "r") as f:
            cabecera = f.readline().strip()
        assert "timestamp" in cabecera
        assert "decibeles" in cabecera
        assert "nivel" in cabecera

    def test_datos_ordenados_por_tiempo(self, tmp_path):
        archivo = str(tmp_path / "test.csv")
        datos = DatasetGenerator.generar_dataset(
            num_registros=100, dias=3, archivo_csv=archivo
        )
        for i in range(len(datos) - 1):
            assert datos[i].timestamp <= datos[i + 1].timestamp

    def test_niveles_validos(self, tmp_path):
        archivo = str(tmp_path / "test.csv")
        datos = DatasetGenerator.generar_dataset(
            num_registros=100, dias=2, archivo_csv=archivo
        )
        niveles_validos = {"bajo", "moderado", "alto", "peligroso"}
        for lectura in datos:
            assert lectura.nivel in niveles_validos

    def test_calculo_db_realista_rango(self):
        from datetime import datetime
        for _ in range(100):
            db = DatasetGenerator._calcular_db_realista("Cafeteria", datetime.now())
            assert 30.0 <= db <= 120.0