// ============================================
// ESP32 - Sensor de Ruido KY-038
// Publica lecturas via MQTT cada 2 segundos
// ============================================

#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* mqtt_server = "broker.hivemq.com"; // Broker público para simulación
const int mqtt_port = 1883;
const char* mqtt_topic = "iot/ruido/sensor01";
const int SOUND_PIN = 34;  // Pin analógico del sensor KY-038
const int LED_PIN = 2;     // LED de alerta (rojo)
const float UMBRAL_ALERTA = 85.0;

WiFiClient espClient;
PubSubClient client(espClient);

// Conectar al WiFi
void setup_wifi() {
  delay(10);
  Serial.println("Conectando a WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado. IP: " + WiFi.localIP().toString());
}

// Reconectar MQTT si se pierde la conexión
void reconnect() {
  while (!client.connected()) {
    Serial.print("Conectando a MQTT...");
    String clientId = "ESP32-Ruido-" + String(random(0xffff), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("conectado!");
    } else {
      Serial.print("Error: ");
      Serial.print(client.state());
      Serial.println(" Reintentando en 5s...");
      delay(5000);
    }
  }
}

float analogToDecibels(int analogValue) {
  return map(analogValue, 0, 4095, 3000, 12000) / 100.0;
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  pinMode(SOUND_PIN, INPUT);
  
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  
  Serial.println("=== Sensor de Ruido IoT Iniciado ===");
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int rawValue = analogRead(SOUND_PIN);
  float decibels = analogToDecibels(rawValue);
  
  String nivel;
  if (decibels < 50) nivel = "bajo";
  else if (decibels < 70) nivel = "moderado";
  else if (decibels < 85) nivel = "alto";
  else nivel = "peligroso";

  digitalWrite(LED_PIN, decibels >= UMBRAL_ALERTA ? HIGH : LOW);

  String payload = "{";
  payload += "\"sensor_id\":\"sensor_01\",";
  payload += "\"ubicacion\":\"Aula_101\",";
  payload += "\"decibeles\":" + String(decibels, 2) + ",";
  payload += "\"nivel\":\"" + nivel + "\",";
  payload += "\"raw_value\":" + String(rawValue);
  payload += "}";

  client.publish(mqtt_topic, payload.c_str());
  
  Serial.println("Publicado: " + payload);

  delay(2000); // Leer cada 2 segundos
}