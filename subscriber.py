import json
from paho.mqtt.client import Client
from cache import cache_message

BROKER = 'localhost'
PORT = 1883
TOPICS = ["Oroville/WML", "Shasta/WML", "Sonoma/WML"]

def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    key = f"{payload['Reservoir']}:{payload['Date']}"
    if cache_message(key, json.dumps(payload)):
        print(f"New data received and cached: {payload}")
    else:
        print(f"Duplicate data skipped: {payload}")

def setup_mqtt():
    client = Client()
    client.on_message = on_message
    client.connect(BROKER, PORT)
    for topic in TOPICS:
        client.subscribe(topic)
    client.loop_forever()

if __name__ == "__main__":
    setup_mqtt()
