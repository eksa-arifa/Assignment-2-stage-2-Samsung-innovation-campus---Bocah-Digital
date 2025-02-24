# IoT Project: Sending Temperature and Humidity Data to Flask and Ubidots

## Description

This project consists of two main components:

1. **ESP32 Client**: Uses a DHT11 sensor to read temperature and humidity data, then sends the data to a Flask server via HTTP POST and to the Ubidots platform via MQTT.
2. **Flask Server**: Receives temperature and humidity data sent by ESP32 and stores it in MongoDB.

## Components

### 1. ESP32 Client

Function: Reads temperature and humidity data from DHT11 sensor, then sends the data to Flask server via HTTP POST and to Ubidots platform using MQTT.

Requirements:
- ESP32
- DHT11 sensor
- WiFi

Process:
- Connects ESP32 to WiFi
- Reads data from DHT11 sensor
- Sends temperature and humidity data to Flask server
- Sends temperature and humidity data to Ubidots via MQTT

### 2. Flask Server

Function: Receives temperature and humidity data sent by ESP32 and stores it in MongoDB.

Requirements:
- Flask
- MongoDB
- Python

Process:
- Receives JSON data through /send_data endpoint
- Stores temperature and humidity data in MongoDB

## Installation and Setup

### 1. Setting up Flask Server with MongoDB

#### Step 1: Prepare Virtual Environment

Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

#### Step 2: Install Dependencies

Install required dependencies with pip:

```bash
pip install flask pymongo python-dotenv
```

#### Step 3: Setup MongoDB

Ensure you have a MongoDB account and database access. You can use MongoDB Atlas or host MongoDB locally.

#### Step 4: Create .env File

Copy the provided .env.example file and rename it to .env. Adjust it with your MongoDB credentials and Flask server configuration.

```bash
cp .env.example .env
```

#### Step 5: Run Flask Server

Run the Flask application with the following command:

```bash
python app.py
```

Flask server will run at http://0.0.0.0:5000.

### 2. Setting up ESP32 Client

#### Step 1: Prepare ESP32

Ensure you have an ESP32 board and active WiFi connection. Use Arduino IDE or other platforms that support MicroPython.

#### Step 2: Install MicroPython

Make sure you have installed MicroPython firmware on ESP32. You can follow the official guide to install it here.

#### Step 3: Install Dependencies

Ensure that umqtt.simple and urequests libraries are available. You can install them via WebREPL or using mpremote if needed.

#### Step 4: Upload Code to ESP32

Upload code from main.py in esp32_client/ folder to your ESP32 board. Don't forget to adjust WiFi and Ubidots parameters in .env file.

#### Step 5: Run Program

Run the program on ESP32 board. This program will read temperature and humidity data from DHT11 sensor and send it to Flask server and Ubidots every 10 seconds.

## Environment Variables Configuration (.env)

To configure credentials and connection settings, create .env file based on the provided .env.example file, and adjust it with your credentials.

### .env File for Flask Server

```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
FLASK_APP_HOST=0.0.0.0
FLASK_APP_PORT=5000
```

### .env File for ESP32 Client

```
WIFI_SSID=your_wifi_ssid
WIFI_PASS=your_wifi_password
FLASK_SERVER_URL=http://your_flask_server_ip:5000/send_data
UBIDOTS_TOKEN=your_ubidots_token
MQTT_BROKER=industrial.api.ubidots.com
DEVICE_LABEL=your_device_label
TEMP_VARIABLE_LABEL=Temperature
HUMIDITY_VARIABLE_LABEL=Humidity
```

## Workflow Explanation

### ESP32 Client:
- Connects to WiFi
- Reads temperature and humidity data from DHT11 sensor
- Sends temperature and humidity data to Flask server using HTTP POST
- Sends data to Ubidots using MQTT

### Flask Server:
- Receives temperature and humidity data from ESP32 at /send_data endpoint
- Stores data in MongoDB

## Troubleshooting

### ESP32 Not Connected to WiFi:
- Ensure your WiFi is active and credentials are correct in .env file
- Check if ESP32 has sufficient signal strength

### Issues with Data Transmission to Flask:
- Check if Flask server is running correctly and can receive data at the correct URL
- Ensure Flask server is reachable from ESP32 device

### Issues with Ubidots Transmission:
- Check if Ubidots token in .env file is correct and can be used to access Ubidots API

## Contributing

If you want to contribute to this project, please fork this repository and create a pull request. Make sure to follow proper development and testing guidelines.

## License

This project is licensed under the MIT License - see <a href="./LICENSE">LICENSE</a> for more details.
