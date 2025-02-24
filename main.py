import network
import time
import machine
import dht
import urequests
from umqtt.simple import MQTTClient

def load_env():
    env_vars = {}
    try:
        with open('/sd/.env', 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    except Exception as e:
        print("Error reading .env file:", e)
    return env_vars

env = load_env()

WIFI_SSID = env.get('WIFI_SSID')
WIFI_PASS = env.get('WIFI_PASS')
FLASK_SERVER_URL = env.get('FLASK_SERVER_URL')
UBIDOTS_TOKEN = env.get('UBIDOTS_TOKEN')
MQTT_BROKER = env.get('MQTT_BROKER')
DEVICE_LABEL = env.get('DEVICE_LABEL')
TEMP_VARIABLE_LABEL = env.get('TEMP_VARIABLE_LABEL')
HUMIDITY_VARIABLE_LABEL = env.get('HUMIDITY_VARIABLE_LABEL')

dht_pin = machine.Pin(18)
dht_sensor = dht.DHT11(dht_pin)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)

    print("Menghubungkan ke WiFi...")
    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")
    print("\nTerhubung ke WiFi!")

def send_data_to_flask(temperature, humidity):
    headers = {'Content-Type': 'application/json'}
    data = {
        'temperature': temperature,
        'humidity': humidity
    }
    
    try:
        response = urequests.post(FLASK_SERVER_URL, json=data, headers=headers)
        print("Data terkirim ke Flask:", response.text)
    except Exception as e:
        print("Error mengirim data ke Flask:", e)

def send_to_ubidots(temperature, humidity):
    client_id = "esp32_" + UBIDOTS_TOKEN[-6:]
    topic = "/v1.6/devices/%s" % DEVICE_LABEL
    payload = '{"%s": {"value": %.2f}, "%s": {"value": %.2f}}' % (TEMP_VARIABLE_LABEL, temperature, HUMIDITY_VARIABLE_LABEL, humidity)
    
    client = MQTTClient(client_id, MQTT_BROKER, user=UBIDOTS_TOKEN, password="", port=1883)
    try:
        client.connect()
        client.publish(topic, payload)
        client.disconnect()
        print("Data terkirim ke Ubidots:", payload)
    except Exception as e:
        print("Error mengirim data ke Ubidots:", e)

connect_wifi()

while True:
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    humidity = dht_sensor.humidity()
    print("Suhu:", temp, "°C")
    print("Kelembapan:", humidity, "%")
    
    send_data_to_flask(temp, humidity)
    send_to_ubidots(temp, humidity)
    
    time.sleep(10)
