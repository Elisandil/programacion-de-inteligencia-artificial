"""
Vista de consola para la aplicación de monitorización de ruido.
"""


class ConsoleView:
    """
    Vista que muestra información en la consola.
    """

    COLORES = {
        "bajo": "\033[92m",       # Verde
        "moderado": "\033[93m",   # Amarillo
        "alto": "\033[91m",       # Rojo claro
        "peligroso": "\033[95m",  # Magenta
        "reset": "\033[0m"        # Reset
    }

    @staticmethod
    def mostrar_banner():
        """Muestra el banner de inicio de la aplicación."""
        print("=" * 60)
        print("MONITOR DE RUIDO AMBIENTAL - IoT Dashboard")
        print("Escuchando mensajes MQTT...")
        print("=" * 60)

    @classmethod
    def mostrar_lectura(cls, data: dict):
        """
        Muestra una lectura de ruido con formato y color.
        """
        nivel = data.get("nivel", "bajo")
        color = cls.COLORES.get(nivel, cls.COLORES["reset"])
        reset = cls.COLORES["reset"]

        print(f"\n{color}{'─' * 50}")
        print(f"  Ubicacion:  {data.get('ubicacion', 'N/A')}")
        print(f"  Decibelios: {data.get('decibeles', 0):.2f} dB")
        print(f"  Nivel:      {nivel.upper()}")
        print(f"  Hora:       {data.get('timestamp', 'N/A')}")
        print(f"  Sensor:     {data.get('sensor_id', 'N/A')}")
        print(f"{'─' * 50}{reset}")

        if nivel == "peligroso":
            print(f"\n{color}  !! ALERTA !! Nivel de ruido PELIGROSO "
                  f"({data.get('decibeles', 0):.2f} dB){reset}\n")

    @staticmethod
    def mostrar_estadisticas(stats: dict):
        print("\nESTADISTICAS:")
        print(f"Total lecturas:     {stats.get('total', 0)}")
        print(f"Promedio:           {stats.get('promedio', 0):.2f} dB")
        print(f"Maximo:             {stats.get('maximo', 0):.2f} dB")
        print(f"Minimo:             {stats.get('minimo', 0):.2f} dB")
        print(f"Alertas peligrosas: {stats.get('alertas', 0)}")

    @staticmethod
    def mostrar_error(mensaje: str):
        print(f"\n\033[91mERROR: {mensaje}\033[0m")

    @staticmethod
    def mostrar_info(mensaje: str):
        print(f"\n\033[94m{mensaje}\033[0m")

    @staticmethod
    def mostrar_guardado_ok():
        print("  Datos guardados en InfluxDB OK")