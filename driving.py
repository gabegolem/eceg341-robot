import machine
import time
import asyncio

class Driving():    
    
    def __init__(self):
        '''-------------------Constants--------------------'''
        self.MAX = 0xffff #self.MAX VALUE of PWM duty is 65536
        self.RIGHT_BIAS = .98 #Right wheel bias 
        self.LEFT_BIAS = .99 #Left wheel bias 

        '''-----------------Motor Settings-----------------'''

        '''
        M1 : Right Motor
        M2 : Left Motor
        A : Forwards
        B : Backwards
        '''
        self.M1A = machine.PWM(machine.Pin(9))
        self.M1B = machine.PWM(machine.Pin(8))
        self.M2A = machine.PWM(machine.Pin(10))
        self.M2B = machine.PWM(machine.Pin(11))

        self.M1A.freq(8_000)
        self.M1B.freq(8_000)
        self.M2A.freq(8_000)
        self.M2B.freq(8_000)


    '''-------------------Functions-------------------'''

    '''stops robot, setting all both motors to 0'''
    def stop(self):
        self.M1A.duty_u16(0)
        self.M2A.duty_u16(0)
        self.M1B.duty_u16(0)
        self.M2B.duty_u16(0)

    '''Basic run function, accepting PWM values for both
    motors. Negative values are read as backwards.
    Functions accounts for specified BIAS'''
    def run(self, M1, M2):

        '''Right motor'''
        if M1 >= 0:
            self.M1A.duty_u16(int(M1*self.RIGHT_BIAS))
            self.M1B.duty_u16(0)
        else: 
            self.M1B.duty_u16(int(-M1*self.RIGHT_BIAS))
            self.M1A.duty_u16(0)

        '''Left motor'''    
        if M2 >= 0:
            self.M2A.duty_u16(int(M2*self.LEFT_BIAS)) 
            self.M2B.duty_u16(0)
        else:
            self.M2B.duty_u16(int(-M2*self.LEFT_BIAS))
            self.M2A.duty_u16(0)

    '''Accelerates gradually over acceleration_time seconds, reducing
    slipping of the wheels from sudden changes in speed, then running at
    final speed for the remainder of the total_time.
    Defaults to 10 slices across .5 seconds, accelerating for 0.1 seconds.'''
    async def gradually_accelerate_async(self, M1vf, M2vf, iterations = 10, acceleration_time = 0.1, total_time = 1):
        '''Reads initial PWM value of each motor'''
        '''Left motor'''
        if self.M2A.duty_u16() > 0:
            M2vi = self.M2A.duty_u16()
        else:
            M2vi = -self.M2B.duty_u16()
        '''Right motor'''
        if self.M1A.duty_u16() > 0:
            M1vi = self.M1A.duty_u16()
        else:
            M1vi = -self.M1B.duty_u16()
        
        '''Determines increment in speed needed for i iterations
        to reach vf'''
        M2increment = (M2vf - M2vi) // iterations
        M1increment = (M1vf - M1vi) // iterations
        
        '''Increments speed for i iterations, gradually changing to vf'''
        for i in range(iterations):
            self.run(M1vi+M1increment*i, M2vi+M2increment*i)
            await asyncio.sleep(acceleration_time / iterations)

        '''Runs at final speed for remaining time'''    
        self.run(M1vf, M2vf)
        await asyncio.sleep(total_time - acceleration_time)

    def gradually_accelerate(self, M1vf, M2vf, iterations = 10, acceleration_time = 0.1, total_time = 1):
        '''Reads initial PWM value of each motor'''
        '''Left motor'''
        if self.M2A.duty_u16() > 0:
            M2vi = self.M2A.duty_u16()
        else:
            M2vi = -self.M2B.duty_u16()
        '''Right motor'''
        if self.M1A.duty_u16() > 0:
            M1vi = self.M1A.duty_u16()
        else:
            M1vi = -self.M1B.duty_u16()
        
        '''Determines increment in speed needed for i iterations
        to reach vf'''
        M2increment = (M2vf - M2vi) // iterations
        M1increment = (M1vf - M1vi) // iterations
        
        '''Increments speed for i iterations, gradually changing to vf'''
        for i in range(iterations):
            self.run(M1vi+M1increment*i, M2vi+M2increment*i)
            time.sleep(acceleration_time / iterations)

        '''Runs at final speed for remaining time'''    
        self.run(M1vf, M2vf)
        time.sleep(total_time - acceleration_time)

    '''Converts a specified speed (cm/s) to PWM value from 0 to 0xffff
    values were determined by modelling robot speed against PWM values'''
    def speedToPWM(self, speed):

        '''Calculates PWM value'''
        coefficient = 1000
        constant = 14000

        if (speed == 0):
            return 0
        
        abs_PWM = coefficient * abs(speed) + constant
        abs_PWM = min(abs_PWM, self.MAX) #Ensures PWM does not exceed self.MAX
        if (speed > 0):
            return abs_PWM
        else:
            return -abs_PWM

    '''Only accepts distances >= 11.43 cm'''
    def distanceToTime(self, distance):

        constant = 11.43 #distance covered during .5 second acceleration
        coefficient = 5.08 #distance covered at max speed over .1 second
        
        time = 0.5 + (0.1 * (distance - constant)/coefficient)
        return time

    '''Drives robot at specified linear_velocity (cm/s)
    and specified angular_velocity (rad/s) for t seconds'''
    def drive_pwm(self, linear_velocity, angular_velocity, acceleration_time=1, total_time = 1):
        '''Diameter between robot wheels, relevant for angular_velocity'''
        length = 13
        
        '''Calculates linear_velocity of each wheel, using equations:
            V_total = (Vl + Vr) / 2
            w = (Vr - Vl) / L'''
        right_velocity = linear_velocity + (angular_velocity*length) / 2
        left_velocity = 2*linear_velocity - right_velocity 
        
        '''Calls gradually accelerate to run motors at specified velocity,
        converting from cm/s to PWM values using speedToPWM'''
        right_pwm = self.speedToPWM(right_velocity)
        left_pwm = self.speedToPWM(left_velocity)
        self.gradually_accelerate(right_pwm, left_pwm, 10, acceleration_time, total_time)
