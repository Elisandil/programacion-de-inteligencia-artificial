"""
Controlador MQTT.
Gestiona la conexión al broker MQTT, la suscripción a topics y el procesamiento de mensajes entrantes con datos de ruido.
"""

import json
import paho.mqtt.client as mqtt
from app.config import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC_SUBSCRIBE
from app.controller.noise_controller import NoiseController
from app.view.console_view import ConsoleView


class MQTTController:
    """
    Controlador que gestiona la comunicación MQTT.
    Se suscribe al topic de ruido y delega el procesamiento al NoiseController siguiendo el patrón MVC.
    """

    def __init__(self):
        """Inicializa el cliente MQTT y los componentes MVC."""
        self.client = mqtt.Client(client_id="python_noise_monitor", protocol=mqtt.MQTTv311)

        # Asignar callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect

        self.noise_controller = NoiseController()
        self.view = ConsoleView()

    def _on_connect(self, client, userdata, flags, rc):
        """
        Callback ejecutado al conectarse al broker.
        """
        if rc == 0:
            self.view.mostrar_info(f"Conectado al broker MQTT ({MQTT_BROKER}:{MQTT_PORT})")
            client.subscribe(MQTT_TOPIC_SUBSCRIBE)
            self.view.mostrar_info(f"Suscrito a: {MQTT_TOPIC_SUBSCRIBE}")
        else:
            self.view.mostrar_error(f"Error de conexión MQTT. Código: {rc}")

    def _on_message(self, client, userdata, msg):
        """
        Callback ejecutado al recibir un mensaje MQTT.
        Parsea el JSON y delega al NoiseController.
        """
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            self.noise_controller.procesar_lectura(payload)
        except json.JSONDecodeError:
            self.view.mostrar_error(f"JSON inválido en topic {msg.topic}")
        except Exception as e:
            self.view.mostrar_error(f"Error procesando mensaje: {e}")

    def _on_disconnect(self, client, userdata, rc):

        if rc != 0:
            self.view.mostrar_error("Desconexión inesperada del broker MQTT")

    def iniciar(self):
        """
        Inicia la conexión MQTT y el bucle de escucha.
        Este método bloquea el hilo principal.
        """
        self.view.mostrar_banner()
        try:
            self.client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
            self.client.loop_forever()
        except ConnectionRefusedError:
            self.view.mostrar_error(
                "No se pudo conectar al broker MQTT. "
                "Está ejecutándose Mosquitto? (docker-compose up)"
            )
        except KeyboardInterrupt:
            self.view.mostrar_info("Deteniendo monitor...")
            self.detener()

    def detener(self):
        self.client.disconnect()
        self.noise_controller.cerrar()
        self.view.mostrar_info("Monitor detenido correctamente.")