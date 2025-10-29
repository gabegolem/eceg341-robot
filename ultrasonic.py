import machine
import neopixel
import time
import my_way

'''Sets up neopixel pins and buzzer'''
NEO_PIN = 18
NUM_PIXELS = 1
buzzer = machine.PWM(machine.Pin(22))
buzzer.freq(4400)
buzzer.duty_u16(1)

pixels = neopixel.NeoPixel(machine.Pin(NEO_PIN), NUM_PIXELS)

class Ultrasound():
    def __init__(self, trigger, echo):
        self.t = trigger
        self.e = echo
    def measure(self):
	 # create trigger pulse
        self.t.low()
        time.sleep_us(2)
        self.t.high()
        time.sleep_us(15)
        self.t.low()
	 # wait for start of echo
        while self.e.value() == 0:
            signaloff = time.ticks_us()
	 # measure echo width
        while self.e.value() == 1:
            signalon = time.ticks_us()
        # compute width
        timepassed = signalon - signaloff
        # return distance
        return timepassed*.034 / 2 # Replace with your calculated values!

note_data = [
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

note_to_freq = {"C": 261, "C#": 277, "D": 294, 
                "D#": 311, "E": 330, "F": 349, 
                "F#": 370, "G": 392, "G#": 415, 
                "A": 440, "A#": 466, "B": 494,
                "R": -1}

def sing(tune=my_way.Songs().get_my_way_lead(), beat=.8, volume=1000):

    for note in tune:
        buzzer.duty_u16(volume)
        pitch = note_to_freq[note[0]]
        octave_offset = note[1]
        duration = note[2]
        if (pitch > 0):
            buzzer.freq(int(pitch * pow(2, octave_offset)))
            time.sleep(duration*beat-.05)
        else:
            buzzer.duty_u16(0)
            time.sleep(duration*beat-.05)
        buzzer.duty_u16(0)
        time.sleep(.05)


