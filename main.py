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

backup_thread = _thread.start_new_thread(ultrasound.sing, (songs.get_my_way_backup, .8, 700))
lead_thread = _thread.start_new_thread(ultrasound.sing, (songs.get_my_way_lead(), .8, 1000))
tests.test_driving()
_thread.exit(backup_thread)
_thread.exit(lead_thread)

ultrasound.sing(songs.get_finish_theme(), beat = 1.2, volume = 1000)
