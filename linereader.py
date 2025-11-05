from machine import Pin
import time
import math

class LineReader():

    def __init__(self):
        self.pins = [Pin(5), Pin(4), Pin(3), Pin(2), Pin(1), Pin(0)]
        self.SAMPLE_NUMBER = 40
        self.DELAY_NUMBER = 15
        self.offset = 0
        self.darkness = 0
        self.confidence = 0

    def reflectance_sample(self, samples, delay_us):
        # charge capacitance
        for pin in self.pins:
            pin.init(Pin.OUT, value=1)

            # change to input
        
        time.sleep_us(10)
        count = [0,0,0,0,0,0]
        for pin in self.pins:
            pin.init(Pin.IN, pull = None)

        for i in range(samples):
            # wait one sample period
            time.sleep_us(delay_us)
            for i,pin in enumerate(self.pins):
                # count the number of 1's
                count[i] += pin.value()    
        # the pulse width is the number of 1's 
        # detected times the delay
        return [c * delay_us for c in count]

    def calculate_position(self, samples, delay_us):
        
        positions = [-20, -12, -4, 4, 12, 20]
        total = 0
        decay = self.reflectance_sample(samples, delay_us)
        
        self.darkness = sum(decay) / (len(self.pins) * samples)

        mean = sum(decay) / len(decay)
        x = 0

        for i,value in enumerate(decay):
            x += ((decay[i] - mean) ** 2)

        variance = x / (len(decay) - 1)
        
        self.confidence = 1 - pow(math.e, -.001 * variance)

        for i in range(len(decay)):
            total -= 15
            total += decay[i]
        
        #Avoid divid by zero error
        if (total == 0):
            return float("inf")

        for i in range(len(decay)):
            decay[i] /= total
            decay[i] *= positions[i]
            
        self.offset = sum(decay)

        return self.offset
    
    def getDarkness(self):
        return self.darkness
    
    def getConfidence(self):
        return self.confidence
