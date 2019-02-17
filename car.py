import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

HERTZ = 100 # Hertz for the PWM control
POWERUPTIME = 0.01 # Time to let motors warm up

class Motor(object):
    '''This class is a bare-bones recreation of the gpiozero
    motor class, and allows the motor to run properly during
    a flask application'''

    def __init__(self, forward, backward):
        self.status = 'off' # Tracks the status of the motor

        self.forwardPin = forward
        self.backwardPin = backward

        GPIO.setup(forward, GPIO.OUT)
        GPIO.setup(backward, GPIO.OUT)

    def get_status(self):
        return self.status

    def forward(self):
        self.status = 'forward'

        GPIO.output(self.forwardPin, GPIO.HIGH)
        GPIO.output(self.backwardPin, GPIO.LOW)

    def backward(self):
        self.status = 'backward'

        GPIO.output(self.forwardPin, GPIO.LOW)
        GPIO.output(self.backwardPin, GPIO.HIGH)

    def stop(self):
        self.status = 'off'

        GPIO.output(self.forwardPin, GPIO.LOW)
        GPIO.output(self.backwardPin, GPIO.LOW)

class PWMMotor(Motor):
    '''This class is similar to the Motor class, but allows for
    precise control of the speed of the motor'''

    def __init__(self, forward, backward):
        super().__init__(forward = forward, backward = backward)
        self.forwardPWM = GPIO.PWM(self.forwardPin, HERTZ)
        self.backwardPWM = GPIO.PWM(self.backwardPin, HERTZ)
        self.forwardPWM.start(0)
        self.backwardPWM.start(0)

    def forward(self, speed = 1):
        self.status = 'forward'

        self.backwardPWM.ChangeDutyCycle(0)
        self.forwardPWM.ChangeDutyCycle(100)

        time.sleep(POWERUPTIME) # Allow motor to receive enough power to start

        self.forwardPWM.ChangeDutyCycle(speed * 100)

    def backward(self, speed = 1):
        self.status = 'backward'

        self.forwardPWM.ChangeDutyCycle(0)
        self.backwardPWM.ChangeDutyCycle(100)
        
        time.sleep(POWERUPTIME) # Allow motor to receive enough power to start

        self.backwardPWM.ChangeDutyCycle(speed * 100)

    def stop(self):
        self.status = 'off'        

        self.forwardPWM.ChangeDutyCycle(0)
        self.backwardPWM.ChangeDutyCycle(0)

class Car:
    '''This class creates an instance of a simple, wheeled robot
    that uses one motor to control forward/backward movement, and
    one motor that controls the steering of the car'''

    def __init__(self, forward, backward, left, right):
        self.driveMotor = Motor(forward = forward, backward = backward)
        self.steerMotor = Motor(forward = left, backward = right)

    def get_status(self):
        drive_status = self.driveMotor.get_status()
        steer_status = self.steerMotor.get_status()

        if steer_status == 'forward':
            steer_status = 'left'
        elif steer_status == 'backward':
            steer_status = 'right'
        else:
            steer_status = 'straight'

        return (drive_status, steer_status)

    def straight(self):
        self.steerMotor.stop()

    def left(self):
        self.steerMotor.forward()

    def right(self):
        self.steerMotor.backward()

    def stop(self):
        self.driveMotor.stop()

    def forward(self):
        self.driveMotor.forward()

    def backward(self):
        self.driveMotor.backward()

class PWMCar(Car):
    '''A modified version of the Car class, that uses a PWM Motor as
    its driver motor'''

    def __init__(self, forward, backward, left, right, speed):
        Car.__init__(self, forward, backward, left, right)
        
        self.driveMotor = PWMMotor(forward, backward)
        self.speed = speed

    def forward(self):
        self.driveMotor.forward(self.speed)

    def backward(self):
        self.driveMotor.backward(self.speed)
