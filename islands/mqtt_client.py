import paho.mqtt.client as mqtt
import ssl
import subprocess
from io import BytesIO
from PIL import Image

def handle_received_data(data):
    print(f"Received data length: {len(data)}")

    image = Image.open(BytesIO(data))
    image.save('received_image.jpg')

# MQTT settings
mqtt_broker_host = "a3lafbeca71eu5-ats.iot.ap-southeast-1.amazonaws.com"
mqtt_broker_port = 8883
mqtt_topic = "back-end-exam"
mqtt_certificate = "certificate.crt"
mqtt_private_key = "private_key.key"
mqtt_root_ca = "root_ca.pem"

mqtt_client = mqtt.Client()

mqtt_client.tls_set(
    ca_certs=mqtt_root_ca,
    certfile=mqtt_certificate,
    keyfile=mqtt_private_key,
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

def on_message(client, userdata, msg):
    handle_received_data(msg.payload)

mqtt_client.on_message = on_message

mqtt_client.connect(mqtt_broker_host, mqtt_broker_port, keepalive=60)

mqtt_client.subscribe(mqtt_topic)

mqtt_client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    mqtt_client.disconnect()
