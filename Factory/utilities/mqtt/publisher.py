'''
File: publisher.py
Project: AIX 2019 Robotics Final Challenge
File Created: Thursday, 18th July 2019 12:42:52 PM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: This class is responsible for publishing any message to a topic. 
-----
Last Modified: Thursday, 18th July 2019 12:42:56 PM
Modified By: nknab
-----
Copyright ©2019 nknab
'''
from config import MQTT as MQTT
import paho.mqtt.client as mqtt


class Publisher:

  # Declaring the MQTT client variable.
    client = None

    """
     * @brief Constructor - Creates an instance of a client and connects to it.
     * 
     * @param host string // Address of the broker.
    """

    def __init__(self, host):
        # Instantiating the MQTT client.
        self.client = mqtt.Client()
        # Connecting to the client.
        self.client.connect(
            host, MQTT['PORT'], MQTT['KEEPALIVE'])

    """
     * @brief Disconnects the client.
     * 
     * @return void
    """

    def disconnect(self):
        self.client.disconnect()

    """
     * @brief Publishes a message to a specific topic.
     * 
     * @param topic string // Topic to publish to.
     * @param msg // Message to be published.
     * 
     * @return void
    """

    def publish(self, topic, msg):
        self.client.publish(topic, msg)
        self.disconnect()
