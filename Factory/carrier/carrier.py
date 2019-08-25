'''
File: carrier.py
Project: AIX 2019 Robotics Final Challenge
File Created: Wednesday, 7th August 2019 4:11:10 PM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: This class is responsible for transporting the crate from the 
       production sector to the delievery zone and vice versa.
-----
Last Modified: Thursday, 8th August 2019 9:34:54 AM
Modified By: nknab
-----
Copyright ©2019 nknab
'''

from utilities import mqtt, movement
from ev3dev2.motor import LargeMotor
from config import Carrier as carrier
from ev3dev2.sensor.lego import TouchSensor


class Carrier:
    # Declaring the various variables.
    motor, production_ts, delivery_ts = None, None, None,

    """
     * @brief Constructor - Initializes the various variables.
    """

    def __init__(self):
        # Instantiating Movement Class.
        self.move = movement.Movement()

        # Instantiating the carrier motor.
        self.motor = LargeMotor(carrier['MOTOR'])

        # Instantiating both touch sensors.
        self.production_ts = TouchSensor(carrier['PRODUCTION_TS'])
        self.delivery_ts = TouchSensor(carrier['DELIVERY_TS'])

    """
     * @brief Move carrier till it comes into contact with a touch sensor.
     * 
     * @param ts TouchSensor // Touch sensor object.
     * @param speed int // Motor speed.
     * 
     * @return void
    """

    def move_till_touch(self, ts, speed):
        while not ts.is_pressed:
            self.move.move_motor(self.motor, speed)
        self.move.stop_motor(self.motor)

    """
     * @brief Resets the carrier to the default position (Production side).
     * 
     * @return void
    """

    def reset(self):
        self.move_till_touch(self.production_ts, -carrier['SPEED'])

    """
     * @brief Subscribes to a topic and returns the data gotten.
     *
     * @param topic string // The topic to be subscribed to.
     * @param condition string // The topic to be subscribed to.
     * 
     * @return void
    """

    def subscribe(self, topic, condition):
        data = ""
        while data != condition:
            sub = mqtt.subscriber.Subscriber(carrier['SERVER'])
            data = sub.subscribe(topic)

    """
    * @brief Publishes a message to a specific topic.
    * 
    * @param topic string // Topic to publish to.
    * @param message // Message to be published.
    * 
    * @return void
    """

    def publish(self, topic, message):
        pub = mqtt.publisher.Publisher(carrier['SERVER'])
        pub.publish(topic, message)

    """
     * @brief Coordinates the entire carrier class to perform the carrier's task.
     *
     * @return void
    """

    def run(self):

        self.reset()

        while True:
            self.subscribe(carrier['CARRIER_TOPIC'], "done")
            self.move_till_touch(self.delivery_ts, carrier['SPEED'])

            self.publish(carrier['CARRIER_TOPIC'], "pickup")
            self.subscribe(carrier['CARRIER_TOPIC'], "ready")

            self.reset()
            self.publish(carrier['CARRIER_TOPIC'], "continue")
