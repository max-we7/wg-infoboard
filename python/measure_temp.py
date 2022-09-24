import adafruit_dht
import board
import time
import datetime
import paho.mqtt.client as mqttClient
dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)


def on_connect(client, userdata, flags, rc):
    if rc == 0:

        print("Connected to broker")

        global Connected  # Use global variable
        Connected = True  # Signal connection

    else:

        print("Connection failed")


broker_address = "192.168.2.39"
port = 1617
user = "mqtt_user"
password = "TiK71xS/G07iO6neX&mA"
Connected = False

client = mqttClient.Client("DHT_Kueche")
client.username_pw_set(user, password=password)
client.on_connect = on_connect
client.connect(broker_address, port=port)
client.loop_start()


while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        output = "Raumtemperatur: {:.1f}°C  |  Luftfeuchtigkeit: {}% ".format(temperature_c, humidity)
        print(output)
        if Connected:
            print("sending values:")
            client.publish("DHT11_Kueche/time_updated", f"{datetime.datetime.now()}")
            client.publish("DHT11_Kueche/temperature", "{:.1f}°C".format(temperature_c))
            client.publish("DHT11_Kueche/humidity", "{}% ".format(humidity))
        with open("../data/temp.txt", "w") as f:
            f.write(output)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()

    time.sleep(1.0)
