# Informe de Pruebas - Monitorización de Ruido IoT

## 1. Resumen

| Métrica           | Valor    |
|-------------------|----------|
| Tests totales     | 21       |
| Tests pasados     | 21       |
| Tests fallidos    | 0        |
| Cobertura aprox.  | 85%      |
| Fecha ejecución   | 07/02/2026 |

## 2. Resultados por Módulo

### 2.1 Modelo (NoiseData) - 11 tests

| Test | Descripción | Resultado |
|------|-------------|-----------|
| test_clasificacion_bajo | dB < 50 → "bajo" | PASS |
| test_clasificacion_moderado | 50 ≤ dB < 70 → "moderado" | PASS |
| test_clasificacion_alto | 70 ≤ dB < 85 → "alto" | PASS |
| test_clasificacion_peligroso | dB ≥ 85 → "peligroso" | PASS |
| test_clasificacion_limite_50 | Exactamente 50 dB | PASS |
| test_clasificacion_limite_85 | Exactamente 85 dB | PASS |
| test_to_dict_contiene_campos | Dict tiene todos los campos | PASS |
| test_to_dict_valores_correctos | Valores coinciden | PASS |
| test_str_format | Formato texto correcto | PASS |
| test_timestamp_automatico | Timestamp se autogenera | PASS |
| test_decibeles_redondeo | Redondeo a 2 decimales | PASS |

### 2.2 Controlador (NoiseController) - 3 tests

| Test | Descripción | Resultado |
|------|-------------|-----------|
| test_procesar_lectura_actualiza_stats | Stats se actualizan | PASS |
| test_procesar_lectura_peligrosa | Alertas se incrementan | PASS |
| test_multiples_lecturas_calcula_maximo | Max/min correctos | PASS |

### 2.3 Generador de Dataset - 7 tests

| Test | Descripción | Resultado |
|------|-------------|-----------|
| test_genera_cantidad_correcta | N registros exactos | PASS |
| test_datos_en_rango_valido | 30-120 dB | PASS |
| test_csv_se_crea | Archivo existe | PASS |
| test_csv_tiene_cabecera | Cabecera correcta | PASS |
| test_datos_ordenados | Orden cronológico | PASS |
| test_niveles_validos | 4 niveles permitidos | PASS |
| test_calculo_db_realista | Valores en rango | PASS |

## 3. Datos de Prueba - Muestra del Dataset

```csv
timestamp,sensor_id,ubicacion,decibeles,nivel
2026-01-31 03:15:22,sensor_03,Biblioteca,32.45,bajo
2026-01-31 09:42:18,sensor_04,Cafeteria,78.91,alto
2026-02-01 11:05:33,sensor_01,Aula_101,62.17,moderado
2026-02-01 14:28:45,sensor_06,Pasillo_Principal,88.34,peligroso
2026-02-02 08:12:09,sensor_05,Laboratorio,71.56,alto
2026-02-03 19:45:11,sensor_03,Biblioteca,38.20,bajo
2026-02-04 10:33:27,sensor_04,Cafeteria,92.78,peligroso
2026-02-05 22:18:44,sensor_02,Aula_102,45.63,bajo