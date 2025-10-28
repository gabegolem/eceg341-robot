import drive
import ultrasonic
import machine
import time
import neopixel

print("Running")


ultrasound = ultrasonic.Ultrasound(trigger = machine.Pin(28, machine.Pin.OUT), echo = machine.Pin(7, machine.Pin.IN))
ultrasonic.sing()

# TEST 1 -- straight!
# 20 cm/s, 0 rad/s 
drive.drive(20, 0, .5)
# stop, drive should have gone 10 cm forward. Check! I got about 12 cm.
drive.drive(0, 0, .5)


# TEST 2 -- reverse
# -20 cm/s, 0 rad/s 
drive.drive(-20, 0, .5)
# stop, drive should have gone 10 cm in reverse. Drive the M1B and M2B pins!
drive.drive(0, 0, .5)


# TEST 3 -- RIGHT
drive.drive(20, math.radian(180), .5)
# stop, drive should have turned about 90 degrees clockwise
drive.drive(0, 0, .5)


# TEST 4 -- LEFT
drive.drive(20, -math.radian(180))
# stop, we should have turned about 180 degrees counter clockwise
drive.drive(0, 0, .5)


# TEST 5 -- ROTATE in PLACE
drive.drive(0, math.radian(360), .5)
# stop, drive should turn about 360 degrees clockwise
drive.drive(0, 0, .5)




'''
while True:        
    distance = ultrasound.measure()
    print(f"Distance = {distance:.2f} cm")
    beep(distance)
    light(distance)
    time.sleep(0.1)
'''

