import machine
import neopixel
import time
import utime
import my_way
import songs
import _thread
import asyncio

class Ultrasound():
    def __init__(self, trigger, echo): 
        '''Sets up neopixel pins and self.buzzer'''
        self.NEO_PIN = 18
        self.NUM_PIXELS =2
        self.pixels = neopixel.NeoPixel(machine.Pin(self.NEO_PIN), self.NUM_PIXELS)
        self.buzzer = machine.PWM(machine.Pin(22))
        self.buzzer.freq(4400)
        self.buzzer.duty_u16(1)
        
        self.t = trigger
        self.e = echo 
        self.note_data = [
            {"note": "C4", "frequency": 261.63, "color_name": "Red", "rgb": (255, 0, 0), "distance_cm": 40},
            {"note": "C#4/Db4", "frequency": 277.18, "color_name": "Orange-Red", "rgb": (255, 69, 0), "distance_cm": 35},
            {"note": "D4", "frequency": 293.66, "color_name": "Orange", "rgb": (255, 140, 0), "distance_cm": 30},
            {"note": "D#4/Eb4", "frequency": 311.13, "color_name": "Yellow", "rgb": (255, 255, 0), "distance_cm": 25},
            {"note": "E4", "frequency": 329.63, "color_name": "Chartreuse", "rgb": (127, 255, 0), "distance_cm": 20},
            {"note": "F4", "frequency": 349.23, "color_name": "Green", "rgb": (0, 255, 0), "distance_cm": 15},
            {"note": "F#4/Gb4", "frequency": 369.99, "color_name": "Spring Green", "rgb": (0, 255, 127), "distance_cm": 10},
            {"note": "G4", "frequency": 392.00, "color_name": "Cyan", "rgb": (0, 255, 255), "distance_cm": 8},
            {"note": "G#4/Ab4", "frequency": 415.30, "color_name": "Azure", "rgb": (0, 127, 255), "distance_cm": 6},
            {"note": "A4", "frequency": 440.00, "color_name": "Blue", "rgb": (0, 0, 255), "distance_cm": 5},
            {"note": "A#4/Bb4", "frequency": 466.16, "color_name": "Violet", "rgb": (139, 0, 255), "distance_cm": 4},
            {"note": "B4", "frequency": 493.88, "color_name": "Magenta", "rgb": (255, 0, 255), "distance_cm": 3}
        ]

        self.theremin_data = [
            {"note": "C4", "frequency": 261.63, "color_name": "Red", "rgb": (127, 0, 0), "distance_cm": 35},
            {"note": "D4", "frequency": 293.66, "color_name": "Orange", "rgb": (127, 70, 0), "distance_cm": 30},
            {"note": "E4", "frequency": 329.63, "color_name": "Chartreuse", "rgb": (58, 127, 0), "distance_cm": 25},
            {"note": "F4", "frequency": 349.23, "color_name": "Green", "rgb": (0, 127, 0), "distance_cm": 20},
            {"note": "G4", "frequency": 392.00, "color_name": "Cyan", "rgb": (0, 127, 127), "distance_cm": 15},
            {"note": "A4", "frequency": 440.00, "color_name": "Blue", "rgb": (0, 0, 127), "distance_cm": 10},
            {"note": "B4", "frequency": 493.88, "color_name": "Magenta", "rgb": (127, 0, 127), "distance_cm": 5},
            {"note": "C5", "frequency": 523, "color_name": "White", "rgb": (127, 127, 127), "distance_cm": 0}
        ]

        self.note_to_freq = {
            "C": 261, "C#": 277, "D": 294, 
            "D#": 311, "E": 330, "F": 349, 
            "F#": 370, "G": 392, "G#": 415, 
            "A": 440, "A#": 466, "B": 494,
            "R": -1
            }
    
    def measure(self):
	 # create trigger pulse
        self.t.low()
        time.sleep_us(2)
        self.t.high()
        time.sleep_us(15)
        self.t.low()
	 # wait for start of echo
        timeout = 250
        start_time = utime.ticks_ms()
        while self.e.value() == 0:
            signaloff = time.ticks_us()
            end_time = utime.ticks_ms()
            elapsed_time = utime.ticks_diff(end_time, start_time)
            if elapsed_time > timeout:
                return 1000

	 # measure echo width
        start_time = utime.ticks_ms()
        while self.e.value() == 1:
            signalon = time.ticks_us()
            end_time = utime.ticks_ms()
            elapsed_time = utime.ticks_diff(end_time, start_time)
            if elapsed_time > timeout:
                return 1000
        # compute width
        timepassed = signalon - signaloff
        # return distance
        return timepassed*.034 / 2
    
    def sing(self, tune, beat, volume):
        for note in tune:
            self.buzzer.duty_u16(volume)
            pitch = self.note_to_freq[note[0]]
            octave_offset = note[1]
            duration = note[2]
            if (pitch > 0):
                self.buzzer.freq(int(pitch * pow(2, octave_offset)))
                time.sleep(duration*beat-.05)
            else:
                self.buzzer.duty_u16(0)
                time.sleep(duration*beat-.05)
            self.buzzer.duty_u16(0)
            time.sleep(.05)
    
    def sing_and_light(self, tune, beat, volume): 
        for note in tune:
            self.buzzer.duty_u16(volume)
            pitch = self.note_to_freq[note[0]]
            octave_offset = note[1]
            duration = note[2]
            if (pitch > 0):
                self.buzzer.freq(int(pitch * pow(2, octave_offset)))
                time.sleep(duration*beat-.05)
            else:
                self.buzzer.duty_u16(0)
                time.sleep(duration*beat-.05)
            self.buzzer.duty_u16(0)
            time.sleep(.05)

    def distance_warning(self, distance):
        self.buzzer.duty_u16(1000)
        for dct in self.note_data:
            if (distance >= dct["distance_cm"]):
                self.buzzer.freq(int(dct["frequency"]))
                self.pixels.fill(dct["rgb"])
                self.pixels.write()
                return
        self.buzzer.duty_u16(0)
        self.pixels.fill((0,0,0))
        self.pixels.write()

    def theremin(self, distance):
        if (distance > 45):
            self.buzzer.duty_u16(0)
            self.pixels.fill((0,0,0))

        self.buzzer.duty_u16(500)
        for dct in self.theremin_data:
            if (distance >= dct["distance_cm"]):
                self.buzzer.freq(int(dct["frequency"]))
                self.pixels.fill(dct["rgb"])
                self.pixels.write()
                return

    def rainbow(self):
        maximum = 20
        minimum = 1
        color = 0
        r = maximum
        g = 0
        b = 0
        while True:
            if (color == 0):
                if (g < maximum):
                    g += 1
                elif (r > minimum):
                    r -= 1
                else:
                    color = 1
            elif (color == 1):
                if (b < maximum):
                    b += 1
                elif (g > minimum):
                    g -= 1
                else:
                    color = 2
            else:
                if (r < maximum):
                    r += 1
                elif (b > minimum):
                    b -= 1
                else:
                    color = 0
                    
            self.pixels.fill((r, g, b))
            self.pixels.write()
            time.sleep(.05)
