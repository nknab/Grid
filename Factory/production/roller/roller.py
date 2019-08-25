'''
File: roller.py
Project: AIX 2019 Robotics Final Challenge
File Created: Friday, 19th July 2019 9:33:33 PM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: This class is responsible for rolling the paper as and when
       the printer needs the paper to be rolled.
-----
Last Modified: Friday, 19th July 2019 9:33:35 PM
Modified By: nknab
-----
Copyright ©2019 nknab
'''

import json

from threading import Thread
from config import Roller as roller
from utilities import mqtt, movement

from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.motor import LargeMotor, MediumMotor


class Roller:
    # Declaring the various variables.
    orders, move, prints_cut, done, track = [], 0, 0, 1, 0
    production_status, roll_status = "continue", ""
    roller_motor, feeder_motor, cut_roller_motor = None, None, None

    cs_one, cs_two, cs_three = None, None, None

    """
     * @brief Constructor - Initializes the various variables.
    """

    def __init__(self):
        # Instantiating Movement Class.
        self.move = movement.Movement()

        # Instantiating the various motors.
        self.roller_motor = LargeMotor(roller['ROLLER_MOTOR'])
        self.feeder_motor = LargeMotor(roller['FEEDER_MOTOR'])
        self.cut_roller_motor = MediumMotor(roller['CUT_ROLLER_MOTOR'])

        # Instantiating the various sensors
        self.cs_one = ColorSensor(roller['CS_ONE'])
        self.cs_two = ColorSensor(roller['CS_TWO'])
        self.cs_three = ColorSensor(roller['CS_THREE'])

    """
     * @brief Subscribes to a topic and returns the data gotten.
     *
     * @param topic string // The topic to be subscribed to.
     *
     * @return data
    """

    def subscribe(self, topic):
        subscriber = mqtt.subscriber.Subscriber(roller['SERVER'])
        data = subscriber.subscribe(topic)

        return data

    """
     * @brief Publishes a message to a specific topic.
     * 
     * @param topic string // Topic to publish to.
     * @param message // Message to be published.
     * 
     * @return void
    """

    def publish(self, topic, message):
        publisher = mqtt.publisher.Publisher(roller['SERVER'])
        publisher.publish(topic, message)

    """
     * @brief Resets the class.
     * 
     * @return void
    """

    def reset(self):
        while True:
            data = self.subscribe(roller['RP_RESET_TOPIC'])

            if data == "reset":
                self.orders.clear()
                self.track, self.done = 0, 1
                self.publish(roller['RP_COLOUR_TOPIC'], "deactivate")

    """
     * @brief Allows the production line to wait for a crate before proceeding.
     * 
     * @return void
    """

    def production(self):
        while True:
            self.production_status = self.subscribe(roller['CARRIER_TOPIC'])

            if self.production_status == "continue":
                self.done = 1
                self.ready()
            else:
                self.done = 0

    """
     * @brief Gets order details from the printer
     * 
     * @return void
    """

    def get_order(self):
        while True:
            # data = json.loads(self.subscribe(roller['RP_ORDER_TOPIC']))
            # self.orders.append(data)
            temp_data = json.loads(self.subscribe(roller['ORDER_TOPIC']))
            order = json.dumps({"OrderID": int(temp_data["orderID"]), "Quantity": int(
                temp_data["quantity"]), "Depot": int(temp_data["depot"])})
            data = json.loads(order)
            self.orders.append(data)
    """
     * @brief Rolls the paper in till it hits the colour sensor.
     * 
     * @param colour_sensor ColorSensor // Colour sensor object
     *
     * @return void
    """

    def roll_till_white(self, colour_sensor):
        while colour_sensor.color != 6:
            self.move.move_motors(
                self.roller_motor, self.cut_roller_motor, -roller['SPEED'], roller['SPEED'])
            self.move.move_motor(self.feeder_motor, -roller['SPEED'])

        self.move.stop_motors(self.roller_motor, self.cut_roller_motor)
        self.move.stop_motor(self.feeder_motor)

    """
     * @brief Coordinates the rolling of the the paper.
     *
     * @return void
    """

    def roll(self):
        state = False
        data = ""
        while data == "":
            data = self.subscribe(roller['RP_ROLL_TOPIC'])

        if data == "roll" and len(self.orders) > 0:
            if self.track == 0:
                self.roll_till_white(self.cs_one)
                self.track += 1
            elif self.track == 1:
                self.roll_till_white(self.cs_two)
                self.track += 1
            else:
                self.publish(roller['RP_COLOUR_TOPIC'], "activate")
                self.roll_till_white(self.cs_three)

            state = True

        elif data == "done":
            self.roll_status = "done"
            self.publish(roller['RP_COLOUR_TOPIC'], "activate")
            self.roll_till_white(self.cs_three)

        return state

    """
     * @brief Alerts the printer that rolling is done.
     *
     * @return void
    """

    def ready(self):
        self.publish(roller['RP_READY_TOPIC'], "ready")

    """
     * @brief Coordinates the with the cutter to cut the paper.
     *
     * @return void
    """

    def cut(self):
        if len(self.orders) > 0:
            self.publish(roller['CUTTER_TOPIC'], "cut")

            data = ""
            while data == "":
                data = self.subscribe(roller['CUTTER_TOPIC'])

            self.orders[0]["Quantity"] -= 1
            if self.roll_status == "done" and self.orders[0]["Quantity"] > 0:
                self.roll_till_white(self.cs_three)
                self.cut()
            else:
                self.roll_status == ""

            db, depot, orderID = "", 0, 0

            for x in self.orders:
                for y in x:
                    if y == "Delivery Bot":
                        db = x[y]
                    elif y == "OrderID":
                        orderID = x[y]
                    elif y == "Depot":
                        depot = x[y]

            self.done = 0
            progress = json.dumps(
                {"OrderID": orderID,  "Status": "Done", "Depot": depot})

            self.publish(roller['DELIVERY_TOPIC'], progress)
            self.publish(roller['CARRIER_TOPIC'], "done")

            # self.orders.clear()
            self.orders.pop(0)

            # Retracting the paper back to the printing platform
            if len(self.orders) <= 0:
                while self.cs_one.color == 6:
                    self.move.move_motors(
                        self.roller_motor, self.cut_roller_motor, roller['SPEED'], -roller['SPEED'])

                    self.move.move_motor(
                        self.feeder_motor, roller['SPEED'])

                self.move.stop_motors(
                    self.roller_motor, self.cut_roller_motor)
                self.move.stop_motor(self.feeder_motor)
                self.track = 0
                self.publish(roller['RP_COLOUR_TOPIC'], "deactivate")

            if self.production_status == "continue" and self.done == 1:
                self.ready()

    """
     * @brief Emergency stop to stop the entire system.
     *
     * @return void
    """

    def emergency_stop(self):
        data = ""
        while data != "stop":
            subscriber = self.subscribe(roller['EMERGENCY_STOP_TOPIC'])
        sys.exit("Emergency Stop Initiated")

    """
     * @brief Coordinates the entire roller class to perform the roller's task.
     *
     * @return void
    """

    def run(self):
        emergency_stop = Thread(target=self.emergency_stop)
        reset = Thread(target=self.reset)
        get_order = Thread(target=self.get_order)
        production = Thread(target=self.production)

        emergency_stop.start()
        reset.start()
        get_order.start()
        production.start()
        state = False

        while True:
            if self.production_status == "continue" and self.done == 1:
                state = self.roll()
                if self.cs_three.color != 6 and state is True:
                    self.ready()
                elif self.cs_three.color == 6:
                    self.cut()
