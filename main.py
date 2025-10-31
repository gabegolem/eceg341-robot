import driving
import ultrasound
import testing
import threading
import songs

print("Running")

songs = songs.Songs()
songs.sing(songs.get_boot_theme(), beat = .6, volume = 1000)

ultrasound = ultrasound.Ultrasound(trigger = machine.Pin(28, machine.Pin.OUT), echo = machine.Pin(7, machine.Pin.IN))
driving = driving.Driving()
tests = testing.Tests()

tests.test_driving()
