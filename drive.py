import machine
import time

'''-------------------Constants--------------------'''
MAX = 0xffff #MAX VALUE of PWM duty is 65536
RIGHT_BIAS = 1 #Right wheel bias 
LEFT_BIAS = .99 #Left wheel bias 

'''-----------------Motor Settings-----------------'''

'''
M1 : Right Motor
M2 : Left Motor
A : Forwards
B : Backwards
'''
M1A = machine.PWM(machine.Pin(9))
M1B = machine.PWM(machine.Pin(8))
M2A = machine.PWM(machine.Pin(10))
M2B = machine.PWM(machine.Pin(11))

M1A.freq(8_000)
M1B.freq(8_000)
M2A.freq(8_000)
M2B.freq(8_000)


'''-------------------Functions-------------------'''

'''stops robot, setting all both motors to 0'''
def stop():
    M1A.duty_u16(0)
    M2A.duty_u16(0)
    M1B.duty_u16(0)
    M2B.duty_u16(0)

'''Basic run function, accepting PWM values for both
motors. Negative values are read as backwards.
Functions accounts for specified BIAS'''
def run(M1, M2):

    '''Right motor'''
    if M1 >= 0:
        M1A.duty_u16(int(M1*RIGHT_BIAS))
        M1B.duty_u16(0)
    else: 
        M1B.duty_u16(int(-M1*RIGHT_BIAS))
        M1A.duty_u16(0)

    '''Left motor'''    
    if M2 >= 0:
        M2A.duty_u16(int(M2*LEFT_BIAS)) 
        M2B.duty_u16(0)
    else:
        M2B.duty_u16(int(-M2*LEFT_BIAS))
        M2A.duty_u16(0)

'''Runs run function for t time'''
def run_time(M1, M2, t):
    run(M1, M2)
    time.sleep(t)

'''Accelerates gradually over t seconds, reducing
slipping of the wheels from sudden changes in speed
Defaults to 10 slices across .5 seconds.'''
def gradually_accelerate(M1vf, M2vf, iterations = 10, t = 0.5):
    
    '''Reads initial PWM value of each motor'''
    '''Left motor'''
    if M2A.duty_u16() > 0:
        M2vi = M2A.duty_u16()
    else:
        M2vi = -M2B.duty_u16()
    '''Right motor'''
    if M1A.duty_u16() > 0:
        M1vi = M1A.duty_u16()
    else:
        M1vi = -M1B.duty_u16()
    
    '''Determines increment in speed needed for i iterations
    to reach vf'''
    M2increment = (M2vf - M2vi) // iterations
    M1increment = (M1vf - M1vi) // iterations

    '''Increments speed for i iterations, gradually changing to vf'''
    for i in range(iterations):
        run_time(M1vi+M1increment*i, M2vi+M2increment*i, t / iterations)

'''Converts a specified speed (cm/s) to PWM value from 0 to 0xffff
values were determined by modelling robot speed against PWM values'''
def speedToPWM(speed):

    '''Calculates PWM value'''
    coefficient = 941
    constant = 12617
    if (speed > 0):
        pwm = coefficient * speed + constant
    else:
        pwm = -(coefficient * abs(speed) + constant)
    
    '''Prevents speed exceeding max PWM value'''
    if (pwm > MAX):
        return MAX
    elif (pwm < -MAX):
        return -MAX

    return pwm

'''Drives robot at specified linear_velocity (cm/s)
and specified angular_velocity (rad/s) for t seconds'''
def drive(linear_velocity, angular_velocity, t=1):

    '''Diameter between robot wheels, relevant for angular_velocity'''
    length = 13
    
    '''Calculates linear_velocity of each wheel, using equations:
        V_total = (Vl + Vr) / 2
        w = (Vr - Vl) / L'''
    right_velocity = linear_velocity + (angular_velocity*length) / 2
    left_velocity = 2*linear_velocity - right_velocity 
    
    '''Calls gradually accelerate to run motors at specified velocity,
    converting from cm/s to PWM values using speedToPWM'''
    gradually_accelerate(speedToPWM(right_velocity), speedToPWM(left_velocity), t)

