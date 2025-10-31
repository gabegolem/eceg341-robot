import driving
import ultrasound
import testing

print("Running")

ultrasound = ultrasound.Ultrasound(trigger = machine.Pin(28, machine.Pin.OUT), echo = machine.Pin(7, machine.Pin.IN))
driving = driving.Driving()
tests = testing.Tests()

tests.test_driving()
