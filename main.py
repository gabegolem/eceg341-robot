import driving
import ultrasound
import testing
import asyncio
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

async def blink(led, period_ms):
    while True:
        led.on()
        await asyncio.sleep_ms(500)
        led.off()
        await asyncio.sleep_ms(period_ms)

async def main(led1, led2):
    asyncio.create_task(blink(led1, 1000))
    asyncio.create_task(blink(led2, 250))
    asyncio.create_task(printy())
    asyncio.create_task(singy())
    await asyncio.sleep_ms(10_000)

async def singy():
    ultrasounder.sing(tunes.get_my_way_lead(), beat = .6, volume = 1000)

async def printy():
    while True:
        print("GAMING OR UNCLEEEEEEE")
        await asyncio.sleep_ms(100)

# Running on a pyboard
asyncio.run(main(machine.Pin(26), machine.Pin(28)))

# Running on a generic board

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
