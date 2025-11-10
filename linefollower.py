from driving import Driving
from linereader import LineReader
import time

class LineFollower:
    def __init__(self, driver: Driving, sensor: LineReader):
        self.driver = driver
        self.sensor = sensor
        
        # PID constants (tune these experimentally)
        self.Kp = 0.08
        self.Ki = 0.0
        self.Kd = 0.02

        # For derivative/integral terms
        self.last_error = 0
        self.integral = 0

        # Basic forward speed in cm/s
        self.base_speed = 12

    def follow_line(self):
        while True:
            offset = self.sensor.calculate_position(
                self.sensor.SAMPLE_NUMBER,
                self.sensor.DELAY_NUMBER
            )

            # Optional: skip updates if confidence is too low
            if self.sensor.getConfidence() < 0.2:
                self.driver.stop()
                continue

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
            angular_velocity = -correction / 10.0  

            # Move robot using combined linear + angular motion
            self.driver.drive_pwm(
                linear_velocity=self.base_speed,
                angular_velocity=angular_velocity,
                total_time=0.1
            )

            time.sleep(0.05)