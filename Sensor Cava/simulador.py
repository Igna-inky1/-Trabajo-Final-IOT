"""Simulador de sensor de cava. Publica temperatura y humedad por MQTT.
Uso: pip install "paho-mqtt>=2"  ->  python simulador.py
"""
import random
import time

import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
INTERVALO = 5  # segundos entre lecturas

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT)
client.loop_start()

temp, hum = 14.0, 70.0
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
