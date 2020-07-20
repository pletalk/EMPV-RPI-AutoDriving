import RPi.GPIO as GPIO

servoPin= 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)

pwm = GPIO.PWM(servoPin, 50)
pwm.start(7)



try:
    while(1):
        position = float(input('servo angle(2.5~12.5) : '))
        pwm.ChangeDutyCycle(position)

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
