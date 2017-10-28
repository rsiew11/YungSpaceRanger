#initial test of the PIR sensor for motion

from picamera import PiCamera
import RPi.GPIO as GPIO
import time

ledPin = 3
pirPin = 21
camera = PiCamera()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pirPin, GPIO.IN)     #PIR sensor
GPIO.setup(ledPin, GPIO.OUT)  #led blinking


#camera.start_preview()
while True:
    pir = GPIO.input(pirPin)
    if (pir):
        GPIO.output(ledPin,1)
        print("klajsdlkajsd;gj")
    else:
        GPIO.output(ledPin,0)
        print(pir)
        print("no shit")
    time.sleep(1)





