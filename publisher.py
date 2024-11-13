import pandas as pd
import json
import time
import sys
import paho.mqtt.client as mqtt

def publish_data(file_path, topic):
    broker = 'localhost'
    client = mqtt.Client()
    client.connect(broker, 1883)

    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        record = {
            "Reservoir": topic.split("/")[0],
            "Date": row["Date"],
            "TAF": row["TAF"]
        }
        client.publish(topic, json.dumps(record))
        print(f"Published: {record}")
        time.sleep(1)
    client.disconnect()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python publisher.py <file_path> <topic>")
        sys.exit(1)
    publish_data(sys.argv[1], sys.argv[2])
