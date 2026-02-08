"""
Punto de entrada principal de la aplicación de monitorización de ruido.
"""

import sys
import json
import time
import paho.mqtt.client as mqtt

from app.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC_PUBLISH
from app.controller.mqtt_controller import MQTTController
from app.utils.dataset_generator import DatasetGenerator
from app.view.console_view import ConsoleView


def modo_monitor():
    """
    Modo 1: Monitor en tiempo real.
    Se conecta al broker MQTT y procesa mensajes entrantes.
    Requiere que Docker Compose esté corriendo.
    """
    controller = MQTTController()
    controller.iniciar()


def modo_simulacion():
    """
    Modo 2: Simulación con datos ficticios.
    Genera un dataset y publica los datos en MQTT simulando
    un sensor real que envía datos cada 0.5 segundos.
    """
    view = ConsoleView()
    view.mostrar_banner()
    view.mostrar_info("Modo SIMULACION - Generando dataset ficticio...")

    datos = DatasetGenerator.generar_dataset(
        num_registros=200,
        dias=7,
        archivo_csv="data/ruido_ficticio.csv"
    )
    view.mostrar_info(f"Dataset generado: {len(datos)} lecturas")
    view.mostrar_info("Publicando datos en MQTT...")

    client = mqtt.Client(client_id="simulador_ruido")
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()

        for lectura in datos:
            payload = json.dumps(lectura.to_dict())
            client.publish(MQTT_TOPIC_PUBLISH, payload)
            view.mostrar_lectura(lectura.to_dict())
            time.sleep(0.5)  # Simular intervalo entre lecturas

    except ConnectionRefusedError:
        view.mostrar_error(
            "No se pudo conectar al broker MQTT.\n"
            "  Ejecuta: docker-compose up -d"
        )
    except KeyboardInterrupt:
        view.mostrar_info("Simulacion detenida por el usuario")
    finally:
        client.loop_stop()
        client.disconnect()


def modo_solo_dataset():
    """
    Modo 3: Solo generar el dataset CSV sin publicar en MQTT.
    Útil para pruebas sin necesidad de infraestructura.
    """
    view = ConsoleView()
    view.mostrar_info("Generando dataset ficticio...")
    datos = DatasetGenerator.generar_dataset(
        num_registros=500,
        dias=7,
        archivo_csv="data/ruido_ficticio.csv"
    )
    view.mostrar_info(f"Dataset generado con {len(datos)} registros")

    dbs = [d.decibeles for d in datos]
    stats = {
        "total": len(datos),
        "promedio": sum(dbs) / len(dbs),
        "maximo": max(dbs),
        "minimo": min(dbs),
        "alertas": sum(1 for d in datos if d.nivel == "peligroso")
    }
    view.mostrar_estadisticas(stats)


if __name__ == "__main__":
    print("\n SISTEMA DE MONITORIZACION DE RUIDO IoT")
    print("=" * 45)
    print("  1. Monitor MQTT (tiempo real)")
    print("  2. Simulacion (datos ficticios + MQTT)")
    print("  3. Solo generar dataset CSV")
    print("=" * 45)

    if len(sys.argv) > 1:
        opcion = sys.argv[1]
    else:
        opcion = input("\nSelecciona modo (1/2/3): ").strip()

    if opcion == "1":
        modo_monitor()
    elif opcion == "2":
        modo_simulacion()
    elif opcion == "3":
        modo_solo_dataset()
    else:
        print("Opcion no valida. Usa 1, 2 o 3.")