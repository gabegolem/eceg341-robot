import driving
import ultrasound
import time
import machine
import math
import neopixel
import songs
import linereading
import linefollowing

class Testing():
    
    def __init__(self):
        self.TRIGGER_PIN = 28
        self.ECHO_PIN = 7

        self.driver = driving.Driving()
        self.ultrasounder = ultrasound.Ultrasound(trigger = machine.Pin(self.TRIGGER_PIN, machine.Pin.OUT), echo = machine.Pin(self.ECHO_PIN, machine.Pin.IN))
        self.singer = songs.Songs()
        self.linereader = linereading.LineReading()
        self.linefollower = linefollowing.LineFollowing(self.driver, self.linereader, self.ultrasounder)

    def test_driving(self):
       
        # TEST 1 -- straight!
        # 20 cm/s, 0 rad/s
        print("TEST 1")
        self.driver.drive_pwm(66, 0, acceleration_time = 3, total_time=3)
        # stop_time, drive should have gone 10 cm forward. Check! I got about 12 cm.
        self.driver.stop_time(1)


        # TEST 2 -- reverse
        # -20 cm/s, 0 rad/s 
        print("TEST 2")
        self.driver.drive_pwm(-20, 0)
        # stop_time, drive should have gone 10 cm in reverse. Drive the M1B and M2B pins!
        self.driver.stop_time(1)


        # TEST 3 -- RIGHT
        print("TEST 3")
        self.driver.drive_pwm(20, math.radians(180))
        # stop_time, drive should have turned about 90 degrees clockwise
        self.driver.stop_time(1)


        # TEST 4 -- LEFT
        print("TEST 4")
        self.driver.drive_pwm(20, -math.radians(180), .5, 1)
        # stop_time, we should have turned about 180 degrees counter clockwise
        self.driver.stop_time(1)


        # TEST 5 -- ROTATE in PLACE
        print("TEST 5")
        self.driver.drive_pwm(0, math.radians(360), .1, 1)
        # stop_time, drive should turn about 360 degrees clockwise
        self.driver.stop_time(1)


    def test_ultrasound(self):

        while True:       
            distance = ultrasound.measure()
            print(f"Distance = {distance:.2f} cm")
            self.ultrasound.distance_warning(distance)
            time.sleep(0.05)
    
    def graph_driving(self):
        MAX = 0xffff
        for i in range(5, 30, 1):
            self.driving.gradually_accelerate(MAX, MAX, 10, 0.5, i/10)
            self.driving.stop_time(8)

    def curl(self, distance_max=40, mult=2/3, t=4):
        self.ultrasounder.clear_neopixel()
        MAX = 0xffff
        distance = 0;
        while (distance < 5):
            distance = self.ultrasounder.measure()
            print(distance)
            time.sleep(.05)
        self.driver.gradually_accelerate(MAX*mult, MAX*mult, 10, t, t)

        distance = self.ultrasounder.measure()
        print(distance)
        print(distance > distance_max)
        while (distance > distance_max):
            distance = self.ultrasounder.measure()
            if (distance < 70 and distance > distance_max):
                self.ultrasounder.rainbow()
            time.sleep(.05)
        self.driver.stop()

    def breakdance(self):
        self.ultrasounder.clear_neopixel()
        self.test_driving()
        self.ultrasounder.rainbow()

    def slalom(self):
        self.linefollower.follow_line()

    def marathon(self):
        self.linefollower.follow_no_crash()
    
    def orienteering(self):
        self.linefollower.follow_no_crash()
        self.ultrasounder.rainbow()

    def luge(self):
        self.linefollower.follow_line()
