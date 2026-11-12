"""Simulador de sensor de cava. Publica temperatura y humedad por MQTT.
Uso: pip install "paho-mqtt>=2"  ->  python simulador.py
"""
import random
import time

import paho.mqtt.client as mqtt

BROKER = "192.168.88.100"  # IP de la máquina virtual con Home Assistant
PORT = 1883
USUARIO = "mqtt"
CLAVE = "cava1234"
INTERVALO = 5  # segundos entre lecturas

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USUARIO, CLAVE)

try:
    client.connect(BROKER, PORT)
except OSError as e:
    print(f"No se pudo conectar a {BROKER}:{PORT} -> {e}")
    print("Revisá que la máquina virtual esté encendida y Mosquitto en ejecución.")
    raise SystemExit(1)

client.loop_start()

temp, hum = 14.0, 70.0
try:
    while True:
        # Deriva suave alrededor de valores normales
        temp += random.uniform(-0.3, 0.3) + (14.0 - temp) * 0.1
        hum += random.uniform(-1, 1) + (70.0 - hum) * 0.1

        # Cada tanto, simula una falla (puerta abierta / compresor roto)
        if random.random() < 0.05:
            temp += random.uniform(4, 6)
            hum -= random.uniform(10, 20)

        client.publish("cava/temperatura", round(temp, 1))
        client.publish("cava/humedad", round(hum, 1))
        print(f"temp={temp:.1f} °C  hum={hum:.1f} %")
        time.sleep(INTERVALO)
except KeyboardInterrupt:
    print("Simulador detenido")
finally:
    client.loop_stop()
    client.disconnect()