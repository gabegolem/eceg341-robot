import driving
import ultrasound
import testing
import _thread
import songs
import linereader
import time

print("Running")


tunes = songs.Songs()
ultrasounder = ultrasound.Ultrasound(trigger = machine.Pin(28, machine.Pin.OUT), echo = machine.Pin(7, machine.Pin.IN))
driver = driving.Driving()
tester = testing.Testing()
follower = linereader.LineReader()

ultrasounder.sing(tunes.get_finish_theme(), beat = .3, volume = 1000)

driver.curling(100)
'''
while True:
    decay = follower.calculate_position(40, 15)
    darkness = follower.getDarkness()
    confidence = follower.getConfidence()
    print(f"Measured decay time: {decay} us.")
    print(f"Darkness: {darkness}")
    print(f"Confidence: {confidence}")
    time.sleep(.5)
'''

'''
#light_thread = _thread.start_new_thread(ultrasounder.rainbow, tuple())
lead_thread = _thread.start_new_thread(ultrasounder.sing, (tunes.get_my_way_lead(), .8, 1000))
#ultrasounder.sing(tune=tunes.get_my_way_lead(), beat=.8, volume=1000)
#ultrasounder.sing(tune=tunes.get_finish_theme(), beat=.3, volume=1000)
tester.test_driving()
'''
