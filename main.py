import driving
import ultrasound
import testing
import asyncio
import songs
import linereading
import linefollowing
import time

print("Running")


tunes = songs.Songs()
ultrasounder = ultrasound.Ultrasound(trigger = machine.Pin(28, machine.Pin.OUT), echo = machine.Pin(7, machine.Pin.IN))
#driver = driving.Driving()
tester = testing.Testing()
#reader = linereader.LineReader()
#follower = linefollower.LineFollower(driver, reader)

ultrasounder.sing(tunes.get_finish_theme(), beat = .3, volume = 1000)

#tester.breakdance()
#tester.curl()
#tester.dash(distance_max = 15, mult=1, t=.5) '''1-m dash'''
#tester.slalom()
#tester.marathon()
#tester.orienteering()
#tester.luge()

def main(test_id):
    if (test_id == 0):
        asyncio.run(tester.breakdance())
    elif (test_id == 1):
        asyncio.run(tester.curl())
    elif (test_id == 2):
        asyncio.run(tester.dash())
    elif (test_id == 3):
        tester.slalom()
    elif (test_id == 4):
        tester.marathon()
    elif (test_id == 5):
        tester.orienteering()
    elif (test_id == 6):
        print("LUGE")
        tester.luge()
    else:
        print(f"No test for id {test_id}")
main(1)

'''
async def singy():
    ultrasounder.sing_async(tunes.get_my_way_lead(), beat = .6, volume = 1000)

async def printy():
    while True:
        print("GAMING OR UNCLEEEEEEE")
        await asyncio.sleep_ms(100)

# Running on a pyboard
asyncio.run(main(1))
'''
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
