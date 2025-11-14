import driving
import ultrasound
import time
import machine
import math
import neopixel

class Testing():
    
    def __init__(self):
        self.TRIGGER_PIN = 28
        self.ECHO_PIN = 7

        self.driver = driving.Driving()
        self.ultrasounder = ultrasound.Ultrasound(trigger = machine.Pin(self.TRIGGER_PIN, machine.Pin.OUT), echo = machine.Pin(self.ECHO_PIN, machine.Pin.IN))

    def test_driving(self):
       
        # TEST 1 -- straight!
        # 20 cm/s, 0 rad/s
        print("TEST 1")
        self.driving.drive(66, 0, acceleration_time = 3, total_time=3)
        # stop_time, drive should have gone 10 cm forward. Check! I got about 12 cm.
        self.driving.stop_time(10)


        # TEST 2 -- reverse
        # -20 cm/s, 0 rad/s 
        print("TEST 2")
        self.driving.drive(-20, 0)
        # stop_time, drive should have gone 10 cm in reverse. Drive the M1B and M2B pins!
        self.driving.stop_time(1)


        # TEST 3 -- RIGHT
        print("TEST 3")
        self.driving.drive(20, math.radians(180))
        # stop_time, drive should have turned about 90 degrees clockwise
        self.driving.stop_time(1)


        # TEST 4 -- LEFT
        print("TEST 4")
        self.driving.drive(20, -math.radians(180), .5, 1)
        # stop_time, we should have turned about 180 degrees counter clockwise
        self.driving.stop_time(1)


        # TEST 5 -- ROTATE in PLACE
        print("TEST 5")
        self.driving.drive(0, math.radians(360), .1, 1)
        # stop_time, drive should turn about 360 degrees clockwise
        self.driving.stop_time(1)


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

    def curling(self):
        MAX = 0xffff
        distance = 0;
        while (distance < 5):
            distance = self.ultrasounder.measure()
            print(distance)
            time.sleep(.05)
        self.driver.gradually_accelerate(MAX, MAX, 10, 5, 5)

        distance = self.ultrasounder.measure()
        print(distance)
        print(distance > 45)
        while (distance > 45):
            print('0')
            distance = self.ultrasounder.measure()
            print('1')
            print(distance)
            time.sleep(.05)
        self.driver.stop()



