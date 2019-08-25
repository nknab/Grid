'''
File: movement.py
Project: AIX 2019 Robotics Final Challenge
File Created: Thursday, 18th July 2019 10:42:01 AM
Author: nknab
Email: kojo.anyinam-boateng@alumni.ashesi.edu.gh
Version: 1.0
Brief: This class is responsible for all the movement of the challenge.
-----
Last Modified: Friday, 19th July 2019 11:20:52 PM
Modified By: nknab
-----
Copyright ©2019 nknab
'''

from math import pi
from threading import Thread


class Movement:

    """
     * @brief Constructor.
    """

    def __init__(self):
        pass

    """
     * @brief Checks if the given speed is within the limits.
     *
     * @param speed int // Speed value to check.
     *
     * @return void
    """
    @staticmethod
    def check_speed(speed):
        if speed > 100:
            speed = 100
        elif speed < -100:
            speed = -100
        return speed

    """
     * @brief Calculate the encoders based on the parameters given.
     *
     * @param radius double // Speed value to check.
     * @param distance double // Speed value to check.
     *
     * @return encoder_ticks
    """

    def calculate_encoder_ticks(self, radius, distance):
        circumference = (2 * pi * radius)
        encoder_ticks = (360 * distance) / circumference

        return encoder_ticks

    """
     * @brief Moves two motors a given distance.
     *
     * @param m MediumMotor/LargeMotor // The motor object.
     * @param speed double // Speed of the motor.
     * @param distance double // The distance the motor should cover.
     * @param radius double // The radius of the wheel or gear.
     * @param brake bool // Determine whether the robot should stop immediately(True) or coast(False).
     * @param wait bool // Determine if it should wait(True) for the action to complete or continue(False).
     *
     * @return void
    """

    def move_motor_distance(self, m, speed, distance, radius, brake, wait):
        validated_speed = self.check_speed(speed)
        encoder_ticks = self.calculate_encoder_ticks(radius, distance)
        m.on_for_degrees(validated_speed, encoder_ticks,
                         brake=brake, block=wait)

    """
     * @brief Turns the motor on forever.
     *
     * @param m MediumMotor/LargeMotor // The motor object.
     * @param speed double // Speed of the motor.
     *
     * @return void
    """

    def move_motor(self, m, speed):
        validated_speed = self.check_speed(speed)
        m.on(validated_speed)

    """
     * @brief Stops the motor.
     *
     * @param m MediumMotor/LargeMotor // The motor object.
     *
     * @return void
    """

    def stop_motor(self, m):
        m.off(brake=True)

    """
     * @brief Run a single motor until it stops moving.
     *
     * @param m MediumMotor/LargeMotor // The motor object.
     *
     * @return void
    """

    def motor_wait(self, m):
        m.wait_until_not_moving()

    """
     * @brief Moves a motor for a given distance.
     *
     * @param m1 MediumMotor/LargeMotor // The motor object.
     * @param m2 MediumMotor/LargeMotor // The motor object.
     * @param m1_speed double // Speed of motor m1.
     * @param m2_speed double // Speed of motor m2.
     * @param m1_distance double // The distance m1 should cover.
     * @param m2_distance double // The distance m2 should cover.
     * @param m1_radius double // The radius of the m1 wheel or gear.
     * @param m2_radius double // The radius of the m2 wheel or gear.
     *
     * @return void
    """

    def move_motors_distance(self, m1, m2, m1_speed, m2_speed, m1_distance, m2_distance, m1_radius, m2_radius):
        validated_m1_speed = self.check_speed(m1_speed)
        validated_m2_speed = self.check_speed(m2_speed)

        m1_thread = Thread(target=self.move_motor_distance(
            m1, validated_m1_speed, m1_distance, m1_radius, True, False))
        m2_thread = Thread(target=self.move_motor_distance(
            m2, validated_m2_speed, m2_distance, m2_radius, True, True))

        m1_thread.start()
        m2_thread.start()

        self.motor_wait(m1)
        self.motor_wait(m2)

        m1_thread.join()
        m2_thread.join()

    """
     * @brief Turns the motor on forever.
     *
     * @param m1 MediumMotor/LargeMotor // The motor object.
     * @param m2 MediumMotor/LargeMotor // The motor object.
     * @param m1_speed double // Speed of motor m1.
     * @param m2_speed double // Speed of motor m2.
     *
     * @return void
    """

    def move_motors(self, m1, m2, m1_speed, m2_speed):
        validated_m1_speed = self.check_speed(m1_speed)
        validated_m2_speed = self.check_speed(m2_speed)

        m1.on(validated_m1_speed)
        m2.on(validated_m2_speed)

    """
     * @brief Stops the motor.
     *
     * @param m1 MediumMotor/LargeMotor // The motor object.
     * @param m2 MediumMotor/LargeMotor // The motor object.
     *
     * @return void
    """

    def stop_motors(self, m1, m2):
        m1.off(brake=True)
        m2.off(brake=True)

    """
     * @brief Run two motors until they stop moving.
     *
     * @param m1 MediumMotor/LargeMotor // The motor object.
     * @param m2 MediumMotor/LargeMotor // The motor object.
     *
     * @return void
    """

    def motors_wait(self, m1, m2):
        m1.wait_until_not_moving()
        m2.wait_until_not_moving()

    """
     * @brief Given a current and target position, it calculates the relative distance and motor direction.
     *
     * @param current double // The current position.
     * @param target double // The target position.
     *
     * @return position, motor_direction
    """

    def calculate_relative_pos(self, current, target):
        position, motor_direction = 0, 1

        if current > target:
            position = current - target
        elif current < target:
            position = target - current
            motor_direction = -1
        elif current == target:
            position = 0

        return position, motor_direction
