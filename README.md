# Summer-school-project-for-posture-analysis-using-Saparate-MQTT-Server
Summer-school-project-for-posture-analysis-using-Saparate-MQTT-Server


import os
import logging
import paho.mqtt.client as mqtt
import base64

# Configuration
broker = 'broker.hivemq.com'
port = 1883
image_topic_pi1 = 'images/pi1'
image_topic_pi2 = 'images/pi2'
image_directory_pi1 = './images_from_pi1/' # can change the directory
image_directory_pi2 = './images_from_pi2/' # can change the directory

# Set up logging
logging.basicConfig(filename='logs/image_receiver.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")
    logging.info(f"Subscribing to topics {image_topic_pi1} and {image_topic_pi2}")
    client.subscribe(image_topic_pi1)
    client.subscribe(image_topic_pi2)

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        image_data = base64.b64decode(msg.payload)
        
        # Determine the correct directory and prefix based on the topic
        if topic == image_topic_pi1:
            image_directory = image_directory_pi1
            prefix = 'p1_'
        elif topic == image_topic_pi2:
            image_directory = image_directory_pi2
            prefix = 'p2_'
        else:
            logging.error(f"Unknown topic: {topic}")
            return
        
        # Get the next image number
        image_number = get_next_image_number(image_directory, prefix)
        image_path = os.path.join(image_directory, f"{prefix}{image_number:02d}.jpg")

        # Save the image
        os.makedirs(image_directory, exist_ok=True)
        with open(image_path, 'wb') as file:
            file.write(image_data)
        
        logging.info(f"Image received and saved to {image_path}")

    except Exception as e:
        logging.error(f"Failed to process message: {e}")

def get_next_image_number(directory, prefix):
    # Get the list of files in the directory
    files = os.listdir(directory)
    # Extract image numbers from file names
    numbers = [int(f.split('_')[1].split('.')[0]) for f in files if f.startswith(prefix) and f.split('_')[1].split('.')[0].isdigit()]
    return max(numbers, default=0) + 1

def main():
    logging.info("Starting MQTT image receiver...")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
