import driving
import ultrasonic
import machine
import time
import neopixel
import math

print("Running")

ultrasound = ultrasonic.Ultrasound(trigger = machine.Pin(28, machine.Pin.OUT), echo = machine.Pin(7, machine.Pin.IN))

# TEST 1 -- straight!
# 20 cm/s, 0 rad/s
print("TEST 1")
driving.drive(20, 0)
# stop_time, drive should have gone 10 cm forward. Check! I got about 12 cm.
driving.stop_time(1)


# TEST 2 -- reverse
# -20 cm/s, 0 rad/s 
print("TEST 2")
driving.drive(-20, 0)
# stop_time, drive should have gone 10 cm in reverse. Drive the M1B and M2B pins!
driving.stop_time(1)


# TEST 3 -- RIGHT
print("TEST 3")
driving.drive(20, math.radians(180))
# stop_time, drive should have turned about 90 degrees clockwise
driving.stop_time(1)


# TEST 4 -- LEFT
print("TEST 4")
driving.drive(20, -math.radians(180))
# stop_time, we should have turned about 180 degrees counter clockwise
driving.stop_time(1)


# TEST 5 -- ROTATE in PLACE
print("TEST 5")
driving.drive(0, math.radians(360))
# stop_time, drive should turn about 360 degrees clockwise
driving.stop_time(1)

ultrasonic.sing()


'''
while True:        
    distance = ultrasound.measure()
    print(f"Distance = {distance:.2f} cm")
    beep(distance)
    light(distance)
    time.sleep(0.1)
'''

