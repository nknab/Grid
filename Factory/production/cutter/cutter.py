'''
File: cutter.py
Project: AIX 2019 Robotics Final Challenge
File Created: Saturday, 10th August 2019 9:56:32 PM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: This class is responsible for cutting the paper once printing 
       is complete.
-----
Last Modified: Saturday, 10th August 2019 10:33:57 PM
Modified By: nknab
-----
Copyright ©2019 nknab
'''

from threading import Thread
from config import Cutter as cutter
from utilities import mqtt, movement

from ev3dev2.motor import LargeMotor, MediumMotor
from ev3dev2.sensor.lego import ColorSensor, TouchSensor


class Cutter:
    # Declaring the various variables.
    move = 0
    fl_motor, cutter_motor, sl_motor, dispenser_motor = None, None, None, None
    cs, lift_ts, cutter_ts = None, None, None
    dispenser_state = False

    """
     * @brief Constructor - Initializes the various variables.
    """

    def __init__(self):
        # Instantiating Movement Class.
        self.move = movement.Movement()

        # Instantiating the various motors.
        self.fl_motor = MediumMotor(cutter['FIRST_LIFT_MOTOR'])
        self.cutter_motor = LargeMotor(cutter['CUTTER_MOTOR'])
        self.sl_motor = MediumMotor(cutter['SECOND_LIFT_MOTOR'])
        self.dispenser_motor = MediumMotor(cutter['DISPENSER_MOTOR'])

        # Instantiating the various sensors
        self.cs = ColorSensor(cutter['CS'])
        self.cutter_ts = TouchSensor(cutter['CUTTER_TS'])
        self.lift_ts = TouchSensor(cutter['LIFT_TS'])

    """
     * @brief Checks if the dispenser motor should be activated or not.
     * 
     * @return void
    """

    def dispenser_status(self):
        while True:
            data = "deactivate"
            subscriber = mqtt.subscriber.Subscriber(cutter['SERVER'])
            data = subscriber.subscribe(cutter['RP_COLOUR_TOPIC'])
            if data == "activate":
                self.dispenser_state = True
            else:
                self.dispenser_state = False
                self.move.stop_motor(self.dispenser_motor)

    """
     * @brief Move dispenser motor till specified condition is met.
     *
     * @param state bool // To determine if it should sense white or not.
     *
     * @return void
    """

    def dispenser(self, state):
        if state:
            while self.cs.color == 6:
                self.move.move_motor(self.dispenser_motor, cutter['SPEED'])
            self.move.stop_motor(self.dispenser_motor)

        elif not state:
            while self.cs.color != 6:
                self.move.move_motor(self.dispenser_motor, cutter['SPEED'])
            self.move.stop_motor(self.dispenser_motor)

    def reset(self):
        self.move.move_motors(self.fl_motor, self.sl_motor,
                              cutter['SPEED'], cutter['SPEED'])
        self.move.motors_wait(self.fl_motor, self.sl_motor)
        self.move.stop_motors(self.fl_motor, self.sl_motor)

        while not self.cutter_ts.is_pressed:
            self.move.move_motor(self.cutter_motor,  cutter['SPEED'])
        self.move.stop_motor(self.cutter_motor)

        self.move.move_motor_distance(
            self.cutter_motor, -cutter['SPEED'], cutter['CUTTER_DISTANCE'], cutter['CUTTER_GEAR_RADIUS'], True, True)
        self.move.stop_motor(self.cutter_motor)

    """
     * @brief Performs the cutting of the paper.
     * 
     * @return void
    """

    def cut(self):
        data = ""
        while data != "cut":
            subscriber = mqtt.subscriber.Subscriber(cutter['SERVER'])
            data = subscriber.subscribe(cutter['CUTTER_TOPIC'])

        # Lift Platform
        while not self.lift_ts.is_pressed:
            self.move.move_motors(
                self.fl_motor, self.sl_motor, -cutter['SPEED'], -cutter['SPEED'])
        self.move.stop_motors(self.fl_motor, self.sl_motor)

        # Cut
        while not self.cutter_ts.is_pressed:
            self.move.move_motor(self.cutter_motor,  cutter['SPEED'])
        self.move.stop_motor(self.cutter_motor)

        # Send Cutter Back
        self.move.move_motor_distance(
            self.cutter_motor, -cutter['SPEED'], cutter['CUTTER_DISTANCE']+2, cutter['CUTTER_GEAR_RADIUS'], True, True)
        self.move.stop_motor(self.cutter_motor)

        # Drop Platform
        self.move.move_motors(self.fl_motor, self.sl_motor,
                              cutter['SPEED'], cutter['SPEED'])
        self.move.motors_wait(self.fl_motor, self.sl_motor)
        self.move.stop_motors(self.fl_motor, self.sl_motor)

        # Position Cutter
        self.move.move_motor_distance(
            self.cutter_motor, cutter['SPEED'], 2, cutter['CUTTER_GEAR_RADIUS'], True, True)
        self.move.stop_motor(self.cutter_motor)

        # Dispense
        self.dispenser(True)

        # Publish Done
        publisher = mqtt.publisher.Publisher(cutter['SERVER'])
        publisher.publish(cutter['CUTTER_TOPIC'], "done")

    """
     * @brief Coordinates the entire cutter class to perform the cutter's task.
     *
     * @return void
    """

    def run(self):
        self.reset()
        dispenser_status = Thread(target=self.dispenser_status)

        dispenser_status.start()

        while True:
            if self.dispenser_state:
                self.dispenser(False)
                self.cut()
            else:
                self.move.stop_motor(self.dispenser_motor)

        # self.cut()
