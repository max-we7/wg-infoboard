import adafruit_dht
import board
import time
dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        output = "Raumtemperatur: {:.1f}°C  |  Feuchtigkeit: {}% ".format(temperature_c, humidity)
        print(output)
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

    time.sleep(1.0)
