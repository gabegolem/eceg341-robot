from driving import Driving
from linereading import LineReading
import ultrasound
import time


'''
Chunky Curvey line
self.Kp = 0.8
self.Ki = 0.0
self.Kd = 0.3
self.sharpness = 9
'''


class LineFollowing:
    def __init__(self, driver: Driving, sensor: LineReader, ultrasounder: Ultrasound):
        self.driver = driver
        self.sensor = sensor
        self.ultrasounder = ultrasounder
        
        # PID constants (tune these experimentally)
        self.Kp = 0.8
        self.Ki = 0.0
        self.Kd = 0.3

        # For derivative/integral terms
        self.last_error = 0
        self.integral = 0

        # Angular Acceleration Correction
        self.sharpness = 7

        # Basic forward speed in cm/s
        self.base_speed = 10

    def follow_line(self):
        while True:
            offset = self.sensor.calculate_position(
                self.sensor.SAMPLE_COUNT,
                self.sensor.SAMPLE_DELAY_US
            )
            '''
            # Optional: skip updates if confidence is too low
            if self.sensor.getConfidence() < 0.2:
                print("TOO LOW")
                self.driver.stop()
                continue
            '''
            # PID computation
            error = offset
            self.integral += error
            derivative = error - self.last_error
            
            correction = (
                self.Kp * error +
                self.Ki * self.integral +
                self.Kd * derivative
            )

            self.last_error = error

            # Convert correction to angular velocity
            # Larger correction means sharper turn
            angular_velocity = -correction / self.sharpness 

            # Move robot using combined linear + angular motion
            self.driver.drive_pwm(
                linear_velocity=self.base_speed,
                angular_velocity=angular_velocity,
                acceleration_time=0.05,
                total_time=0.05
            )

            time.sleep(0.01)

    def follow_no_crash(self):
        start = time.time()
        while True:
            offset = self.sensor.calculate_position(
                self.sensor.SAMPLE_COUNT,
                self.sensor.SAMPLE_DELAY_US
            )
            '''
            # Optional: skip updates if confidence is too low
            if self.sensor.getConfidence() < 0.2:
                print("TOO LOW")
                self.driver.stop()
                continue
            '''
            # PID computation
            error = offset
            self.integral += error
            derivative = error - self.last_error
            
            correction = (
                self.Kp * error +
                self.Ki * self.integral +
                self.Kd * derivative
            )

            self.last_error = error

            # Convert correction to angular velocity
            # Larger correction means sharper turn
            angular_velocity = -correction / self.sharpness 

            # Move robot using combined linear + angular motion
            self.driver.drive_pwm(
                linear_velocity=self.base_speed,
                angular_velocity=angular_velocity,
                acceleration_time=0.05,
                total_time=0.05
                )

            time.sleep(0.01)

            if (self.ultrasounder.measure() < 10):
                self.driver.stop_time(100)

            end = time.time()
            if (end-start > 10):
                self.driver.stop_time(100)

