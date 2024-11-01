import paho.mqtt.client as mqtt
from gpiozero import LED
from time import sleep

# Configuration
broker = '192.168.1.79'
port = 1883
topic = 'posture_info'

# Setup LEDs
red_led = LED(17)    # GPIO 17 for Red LED
orange_led = LED(27) # GPIO 27 for Orange LED
green_led = LED(22)  # GPIO 22 for Green LED

def turn_off_all_leds():
    red_led.off()
    orange_led.off()
    green_led.off()

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    try:
        message = msg.payload.decode()
        print(f"Received message: {message}")
        
        # Turn off all LEDs before setting the new state
        turn_off_all_leds()
        
        if message == '1':
            red_led.on()
        elif message == '-1':
            orange_led.on()
        elif message == '0':
            green_led.on()
        else:
            print(f"Unknown message: {message}")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
