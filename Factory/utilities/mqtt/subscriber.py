'''
File: subscriber.py
Project: AIX 2019 Robotics Final Challenge
File Created: Thursday, 18th July 2019 12:54:36 PM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: This class is responsible for subscribing to any topic and. 
       retrieving the data associated with it.
-----
Last Modified: Thursday, 18th July 2019 12:54:41 PM
Modified By: nknab
-----
Copyright ©2019 nknab
'''


from config import MQTT as MQTT
import paho.mqtt.client as mqtt


class Subscriber:

    # The topic to be subscribed to.
    # The message from the topic.
    # client variable.
    topic, data, client = None, None, None

    """
     * @brief Constructor - it creates an instance of a client and connects to it.
     *
     * @param host // The address of the broker.
    """

    def __init__(self, host):
        self.client = mqtt.Client()
        self.client.connect(
            host, MQTT['PORT'], MQTT['KEEPALIVE'])

    """
     * @brief This subscribes to a specified topic.
     *
     * @param client mqtt.Client // The mqtt client instance.
     * @param userdata //The callback.
     * @param flags // A dict that contains response flags from the broker.
     * @param rc // Indicates if the connection was successful or not.
     *
     * @return void
    """

    def on_connect(self, client, userdata, flags, rc):
        self.client.subscribe(self.topic, 1)

    """
     * @brief This gets the message from the subscribe topic.
     *
     * @param client mqtt.Client // The mqtt client instance.
     * @param userdata //The callback.
     * @param msg // The message.
     *
     * @return void
    """

    def on_message(self, client, userdata, msg):
        self.data = msg.payload.decode("utf-8")

    """
     * @brief This disconnects the client.
     * 
     * @return void
    """

    def disconnect(self):
        self.client.disconnect()

    """
     * @brief This the main method of the class that coordinates everything.
     *
     * @param topic string // The topic to be subscribed to.
     *
     * @return data
    """

    def subscribe(self, topic):
        self.topic = topic

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        while self.data == None:
            self.client.loop()

        self.client.loop_stop()
        self.disconnect()
        return self.data
