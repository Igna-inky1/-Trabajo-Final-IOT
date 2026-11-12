Monitor de cava con IoT
docker compose up -d
Entrar a http://localhost:8123, crear el usuario y agregar la integración MQTT (host mosquitto, puerto 1883).
pip install "paho-mqtt>=2" y python simulador.py
En Home Assistant aparecen sensor.cava_temperatura y sensor.cava_humedad; las alertas saltan como notificaciones.
Grafana en http://localhost:3000 (admin/admin): agregar datasource PostgreSQL (host postgres:5432, db homeassistant, user/pass ha, TLS disable).
Query de ejemplo para el gráfico de temperatura:

SELECT s.last_updated_ts AS "time", s.state::float AS temperatura
FROM states s
JOIN states_meta m ON s.metadata_id = m.metadata_id
WHERE m.entity_id = 'sensor.cava_temperatura'
  AND s.state NOT IN ('unknown', 'unavailable')
  AND $__unixEpochFilter(s.last_updated_ts)
ORDER BY 1;
