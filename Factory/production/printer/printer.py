'''
File: printer.py
Project: AIX 2019 Robotics Final Challenge
File Created: Thursday, 18th July 2019 11:46:48 AM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: This class is responsible for receiveing the design to be printed and
       actually printing the design unto the paper.
-----
Last Modified: Thursday, 18th July 2019 11:46:51 AM
Modified By: nknab
-----
Copyright ©2019 nknab
'''

import sys
import json

from threading import Thread
from utilities import mqtt, movement
from config import Printer as printer

from ev3dev2.sensor.lego import TouchSensor
from ev3dev2.motor import LargeMotor, MediumMotor


class Printer:
    # Declaring the various variables.
    orders, move, x_position, y_position = [], 0, 0, 0
    x_axis_motor, y_axis_motor, lift_motor, grabber_motor = None, None, None, None

    """
     * @brief Constructor - Initializes the various variables.
    """

    def __init__(self):
        # Instantiating Movement Class.
        self.move = movement.Movement()

        # Instantiating the various motors.
        self.x_axis_motor = LargeMotor(printer['X_AXIS_MOTOR'])
        self.y_axis_motor = LargeMotor(printer['Y_AXIS_MOTOR'])
        self.lift_motor = MediumMotor(printer['Z_AXIS_MOTOR'])
        self.grabber_motor = MediumMotor(printer['GRABBER_MOTOR'])

    """
     * @brief Resets the x-axis motor back to position 0, 0.
     * 
     * @return void
    """

    def reset_x(self):
        x_axis_ts = TouchSensor(printer['X_AXIS_TS'])
        while not x_axis_ts.is_pressed:
            self.move.move_motor(self.x_axis_motor, printer['SPEED'])
        self.move.stop_motor(self.x_axis_motor)

    """
     * @brief Resets the y-axis motor back to position 0, 0.
     * 
     * @return void
    """

    def reset_y(self):
        y_axis_ts = TouchSensor(printer['Y_AXIS_TS'])
        while not y_axis_ts.is_pressed:
            self.move.move_motor(self.y_axis_motor, printer['SPEED'])
        self.move.stop_motor(self.y_axis_motor)

    """
     * @brief Resets both x and y-axis motors back to position 0, 0.
     * 
     * @return void
    """

    def reset(self):
        self.move.move_motors(
            self.lift_motor, self.grabber_motor, -printer['SPEED'], printer['SPEED'])

        self.move.motors_wait(self.lift_motor, self.grabber_motor)

        self.move.stop_motors(self.lift_motor, self.grabber_motor)

        x_thread = Thread(target=self.reset_x)
        y_thread = Thread(target=self.reset_y)

        x_thread.start()
        y_thread.start()

        x_thread.join()
        y_thread.join()

    """
     * @brief Gets order details from Grid (web application).
     * 
     * @return void
    """

    def get_order(self):
        while True:
            subscriber = mqtt.subscriber.Subscriber(printer['SERVER'])
            data = json.loads(subscriber.subscribe(
                printer['ORDER_TOPIC']))

            # order = json.dumps({"OrderID": int(data["orderID"]), "Quantity": int(
            #     data["quantity"]), "Depot": int(data["depot"])})

            # publisher = mqtt.publisher.Publisher(printer['SERVER'])
            # publisher.publish(printer['RP_ORDER_TOPIC'], order)

            self.orders.append(data)

    """
     * @brief To get or drop the stamp.
     * 
     * @param x_position double // Current x position.
     * @param y_position double// Current y position.
     * @param speed double // Speed of the motor.
     * @param mode int// Determine whether to pick (1) or drop stamp (-1).
     * @param stamp_position int// Stamp position to go to.
     * 
     * @return x_pos, y_pos // Current xy position.
    """

    def get_or_leave_stamp(self, x_position, y_position, speed, mode, stamp_position):
        x_rel_position, x_direction = self.move.calculate_relative_pos(
            x_position, printer['STAMP_POSITION'][stamp_position][0])
        y_rel_position, y_direction = self.move.calculate_relative_pos(
            y_position, printer['STAMP_POSITION'][stamp_position][1])

        x_pos, y_pos = printer['STAMP_POSITION'][stamp_position][0], printer['STAMP_POSITION'][stamp_position][1]

        self.move.move_motors_distance(self.x_axis_motor, self.y_axis_motor, speed*x_direction, speed*y_direction, x_rel_position,
                                       y_rel_position, printer['X_AXIS_GEAR_RADIUS'], printer['Y_AXIS_GEAR_RADIUS'])

        # Get the stamp
        if mode == 1:
            # Open Grabber
            self.move.move_motor_distance(
                self.grabber_motor, -speed, printer['MAX_OPEN_GRABBER_DISTANCE'], printer['GRABBER_GEAR_RADIUS'], True, True)
            self.move.motor_wait(self.grabber_motor)
            self.move.stop_motor(self.grabber_motor)

            # Drop the Grabber
            self.move.move_motor_distance(
                self.lift_motor, speed, printer['Z_AXIS_DROP_LIFT_DISTANCE'], printer['LIFT_GEAR_RADIUS'], True, True)
            self.move.motor_wait(self.lift_motor)
            self.move.stop_motor(self.lift_motor)

            # Close the Grabber
            self.move.move_motor(self.grabber_motor, printer['SPEED'])
            self.move.motor_wait(self.grabber_motor)
            self.move.stop_motor(self.grabber_motor)

            # Lift the Grabber
            self.move.move_motor_distance(
                self.lift_motor, -speed, printer['Z_AXIS_DROP_LIFT_DISTANCE'], printer['LIFT_GEAR_RADIUS'], True, True)
            self.move.motor_wait(self.lift_motor)
            self.move.stop_motor(self.lift_motor)

        # Drop the stamp.
        elif mode == -1:
            # Drop the Grabber
            self.move.move_motor_distance(
                self.lift_motor, speed, printer['Z_AXIS_DROP_LIFT_DISTANCE'], printer['LIFT_GEAR_RADIUS'], True, True)
            self.move.motor_wait(self.lift_motor)
            self.move.stop_motor(self.lift_motor)

            # Open Grabber
            self.move.move_motor_distance(
                self.grabber_motor, -speed, printer['MAX_OPEN_GRABBER_DISTANCE'], printer['GRABBER_GEAR_RADIUS'], True, True)
            self.move.motor_wait(self.grabber_motor)
            self.move.stop_motor(self.grabber_motor)

            # Lift the Grabber
            self.move.move_motor_distance(
                self.lift_motor, -speed, printer['Z_AXIS_DROP_LIFT_DISTANCE'], printer['LIFT_GEAR_RADIUS'], True, True)
            self.move.motor_wait(self.lift_motor)
            self.move.stop_motor(self.lift_motor)

            # Close the Grabber
            self.move.move_motor_distance(
                self.grabber_motor, speed, printer['MAX_OPEN_GRABBER_DISTANCE'], printer['GRABBER_GEAR_RADIUS'], True, True)
            self.move.motor_wait(self.grabber_motor)
            self.move.stop_motor(self.grabber_motor)

        return x_pos, y_pos

    """
     * @brief Stamp the paper with the stamp obtained.
     * 
     * @param speed double // Speed of the motor.
     * 
     * @return void
    """

    def stamp(self, speed):
        self.move.move_motor_distance(
            self.lift_motor, speed, printer['PRINTING_Z_DISTANCE'], printer['LIFT_GEAR_RADIUS'], True, True)

        self.move.move_motor_distance(
            self.lift_motor, -speed, printer['PRINTING_Z_DISTANCE'], printer['LIFT_GEAR_RADIUS'], True, True)

    """
     * @brief To get or drop the stamp.
     * 
     * @param x_position double // Current x position.
     * @param y_position double// Current y position.
     * @param pattern int array // Positions where the stamps should be placed on the paper.
     * @param stamp_position int// Stamp position to go to.
     * 
     * @return x_position, y_position // Current xy position.
    """

    def printing(self, x_position, y_position, pattern, stamp_position):

        x_position, y_position = self.get_or_leave_stamp(
            x_position, y_position, printer['SPEED'], 1, stamp_position)

        for position in pattern:
            x_rel_position, x_direction = self.move.calculate_relative_pos(
                x_position, printer['PRINT_POSITION'][position][0])
            y_rel_position, y_direction = self.move.calculate_relative_pos(
                y_position, printer['PRINT_POSITION'][position][1])

            x_position, y_position = printer['PRINT_POSITION'][
                position][0], printer['PRINT_POSITION'][position][1]

            self.move.move_motors_distance(self.x_axis_motor, self.y_axis_motor, printer['SPEED']*x_direction, printer['SPEED']*y_direction, x_rel_position,
                                           y_rel_position, printer['X_AXIS_GEAR_RADIUS'], printer['Y_AXIS_GEAR_RADIUS'])

            self.stamp(printer['SPEED'])

        x_position, y_position = self.get_or_leave_stamp(
            x_position, y_position, printer['SPEED'], -1, stamp_position)

        return x_position, y_position

    """
     * @brief Stamping the paper according to the print matrix.
     * 
     * @return void
    """

    def process_order(self):
        if len(self.orders) > 0:
            count = 0
            pattern_one, pattern_two, pattern_three, pattern_four = [], [], [], []

            status = json.dumps(
                {"OrderID": int(self.orders[0]["orderID"]), "Status": "Production"})

            publisher = mqtt.publisher.Publisher(printer['SERVER'])
            publisher.publish(printer['STATUS_TOPIC'], status)

            # Generating the pattern matrix for each of the stamps
            for x in self.orders[0]["print_matrix"]:
                for y in x:
                    if y == 1:
                        pattern_one.append(count)
                    elif y == 2:
                        pattern_two.append(count)
                    elif y == 3:
                        pattern_three.append(count)
                    elif y == 4:
                        pattern_four.append(count)

                    count += 1

            count = 0
            while count < int(self.orders[0]["quantity"]):
                publisher = mqtt.publisher.Publisher(printer['SERVER'])
                publisher.publish(printer['RP_ROLL_TOPIC'], "roll")

                data = ""
                while data != "ready":
                    subscriber = mqtt.subscriber.Subscriber(printer['SERVER'])
                    data = subscriber.subscribe(
                        printer['RP_READY_TOPIC'])

                if len(pattern_one) > 0:
                    self.x_position, self.y_position = self.printing(
                        self.x_position, self.y_position, pattern_one, 0)
                if len(pattern_two) > 0:
                    self.x_position, self.y_position = self.printing(
                        self.x_position, self.y_position, pattern_two, 1)
                if len(pattern_three) > 0:
                    self.x_position, self.y_position = self.printing(
                        self.x_position, self.y_position, pattern_three, 2)
                if len(pattern_four) > 0:
                    self.x_position, self.y_position = self.printing(
                        self.x_position, self.y_position, pattern_four, 3)

                count += 1

                if count == int(self.orders[0]["quantity"]):
                    publisher = mqtt.publisher.Publisher(printer['SERVER'])
                    publisher.publish(printer['RP_ROLL_TOPIC'], "done")

            self.orders.pop(0)
            self.reset()
            self.x_position, self.y_position = 0, 0

    """
     * @brief Emergency stop to stop the entire system.
     *
     * @return void
    """

    def emergency_stop(self):
        data = ""
        while data != "stop":
            subscriber = mqtt.subscriber.Subscriber(printer['SERVER'])
            data = subscriber.subscribe(printer['EMERGENCY_STOP_TOPIC'])

        sys.exit("Emergency Stop Initiated")

    """
     * @brief Coordinates the entire printer class to perform the printer's task.
     *
     * @return void
    """

    def run(self):
        self.reset()

        emergency_stop = Thread(target=self.emergency_stop)
        get_orders = Thread(target=self.get_order)

        get_orders.start()
        emergency_stop.start()

        while True:
            self.process_order()
