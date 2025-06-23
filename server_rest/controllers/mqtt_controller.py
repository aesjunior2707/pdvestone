import paho.mqtt.client as mqtt

class MQTTController:
    def __init__(self,serial):
        self.broker = 'localhost'
        self.port = 1883
        self.serial = serial
        self.client = mqtt.Client()

    def connect(self):
        try:
            self.client.connect(self.broker, self.port)
            print(f"Connected to MQTT broker at {self.broker}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to MQTT broker: {e}")

    def publish(self, topic, message):
        try:
            self.client.publish(topic, message)
            print(f"Published message '{message}' to topic '{topic}'")
        except Exception as e:
            print(f"Failed to publish message: {e}")

    def disconnect(self):
        try:
            self.client.disconnect()
            print("Disconnected from MQTT broker")
        except Exception as e:
            print(f"Failed to disconnect: {e}")

# Example usage:
# mqtt_controller = MQTTController("mqtt.example.com")
# mqtt_controller.connect()
# mqtt_controller.publish("test/topic", "Hello, MQTT!")
# mqtt_controller.disconnect()