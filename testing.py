import driving
import ultrasound
import time
import machine
import math
import neopixel
import songs
import linereading
import linefollowing
import asyncio

class Testing():
    
    def __init__(self):
        self.TRIGGER_PIN = 28
        self.ECHO_PIN = 7
        self.MAX = 0xffff

        self.driver = driving.Driving()
        self.ultrasounder = ultrasound.Ultrasound(trigger = machine.Pin(self.TRIGGER_PIN, machine.Pin.OUT), echo = machine.Pin(self.ECHO_PIN, machine.Pin.IN))
        self.singer = songs.Songs()
        self.linereader = linereading.LineReading()
        self.linefollower = linefollowing.LineFollowing(self.driver, self.linereader, self.ultrasounder)


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

    async def curl(self, distance_max=40, mult=2/3, t=4):
        self.ultrasounder.clear_neopixel()
        light_max = 70
        
        MAX = 0xffff
        distance = 0
        while (distance < 5):
            distance = self.ultrasounder.measure()
            print(distance)
            time.sleep(.05)
        self.driver.gradually_accelerate(MAX*mult, MAX*mult, 10, t, t)

        distance = self.ultrasounder.measure()

        while (distance > distance_max):
            distance = self.ultrasounder.measure()
            if (distance < light_max and distance > distance_max):
                asyncio.create_task(self.ultrasounder.rainbow())
            asyncio.sleep(.05)
            time.sleep(.05)
        self.driver.stop()

    async def breakdance(self):
        self.ultrasounder.clear_neopixel()
        asyncio.create_task(self.driver.gradually_accelerate_async(self.MAX,self.MAX,10,10))
        asyncio.create_task(self.ultrasounder.rainbow())
        asyncio.create_task(self.ultrasounder.sing_async(self.singer.get_my_way_lead(), beat = .8, volume = 1000))
        await asyncio.sleep(100)

    async def dash():
        
        distance_max = 20

        distance = 0
        while (distance < 5):
            distance = self.ultrasounder.measure()
            time.sleep(.05)
        self.driver.gradually_accelerate(self.MAX, self.MAX, 1, 1)

        distance = ultrasounder.measure()

        while(distance > distance_max):
            distance = self.ultrasounder.measure()
            time.sleep(.05)
        self.driver.stop()

    def slalom(self):
        self.linefollower.follow_line()

    def marathon(self):
        self.linefollower.follow_no_crash()
    
    def orienteering(self):
        self.linefollower.follow_no_crash()
        self.ultrasounder.rainbow()

    def luge(self):
        self.linefollower.follow_line()
