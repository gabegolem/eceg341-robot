import driving
import ultrasound
import testing
import _thread
import songs

print("Running")


songs = songs.Songs()
ultrasound = ultrasound.Ultrasound(trigger = machine.Pin(28, machine.Pin.OUT), echo = machine.Pin(7, machine.Pin.IN))
driving = driving.Driving()
tests = testing.Tests()

ultrasound.sing(songs.get_boot_theme(), beat = .6, volume = 1000)

light_thread = _thread.start_new_thread(ultrasound.rainbow, tuple())
#lead_thread = _thread.start_new_thread(ultrasound.sing, (songs.get_my_way_lead(), .8, 1000))
#ultrasound.sing(tune=songs.get_my_way_lead(), beat=.8, volume=1000)
ultrasound.sing(tune=songs.get_finish_theme(), beat=.3, volume=1000)
#tests.test_driving()
