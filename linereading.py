from machine import Pin
import time
import math

class LineReading():

    def __init__(self):
        # 6 reflectance sensors arranged left-to-right
        self.pins = [Pin(i) for i in range(5, -1, -1)]  # Pins 5 → 0
        self.SAMPLE_COUNT = 10      # Number of samples per reading
        self.SAMPLE_DELAY_US = 15   # Delay between samples (microseconds)
        
        # Metrics computed from readings
        self.offset = 0.0           # Lateral offset of line (negative = left)
        self.darkness = 0.0         # How much of line is seen
        self.confidence = 0.0       # Confidence in reading
        
        # The minimum reading tends to be 15 not 0
        self.READING_CORRECTION = 15

    def reflectance_sample(self, samples, delay_us):
        # charge capacitance
        for pin in self.pins:
            pin.init(Pin.OUT, value=1)

            # change to input
        time.sleep_us(10)
        
        for pin in self.pins:
            pin.init(Pin.IN, pull = None)

        counts = [0] * len(self.pins)
        for i in range(samples):
            # wait one sample period
            time.sleep_us(delay_us)
            for i,pin in enumerate(self.pins):
                # count the number of 1's
                counts[i] += pin.value()    
        # the pulse width is the number of 1's 
        # detected times the delay
        return [c * delay_us for c in counts]

    def calculate_position(self, samples=None, delay_us=None):
        samples = samples or self.SAMPLE_COUNT
        delay_us = delay_us or self.SAMPLE_DELAY_US

        sensor_positions = [-20, -12, -4, 4, 12, 20]
        readings = self.reflectance_sample(samples, delay_us)
        adjusted_readings = [max(0, r - self.READING_CORRECTION) for r in readings]
        total_reflectance = sum(adjusted_readings)
        mean_val = total_reflectance / len(adjusted_readings)

        # Supposedly tells us how much of the line the sensor sees
        self.darkness = mean_val / samples

        variance = sum((r - mean_val) ** 2 for r in adjusted_readings) / (len(adjusted_readings) - 1)
        self.confidence = 1 - math.exp(-0.001 * variance)  # higher variance → higher confidence

        if total_reflectance == 0:
            return .00001  # Avoid divide-by-zero

        normalized = [r / total_reflectance for r in adjusted_readings]

        # Weighted sum to get estimated line offset
        weighted_sum = sum(p * n for p, n in zip(sensor_positions, normalized))
        self.offset = weighted_sum

        print(self.offset)
        
        return self.offset
    
    def getDarkness(self):
        return self.darkness
    
    def getConfidence(self):
        return self.confidence

    def getSampleCount(self):
        return self.SAMPLE_COUNT

    def getSampleDelay(self):
        return self.SAMPLE_DELAY_US
