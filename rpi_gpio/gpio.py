
import time
import datetime
import RPi.GPIO as GPIO

RPI3_GPIO_OUTPUT=2

GPIO.setmode(GPIO.BCM)
GPIO.setup(RPI3_GPIO_OUTPUT, GPIO.OUT)

for x in range(100):

    print(str(datetime.datetime.now(datetime.timezone.utc).isoformat()) + ' Low')
    GPIO.output(RPI3_GPIO_OUTPUT, GPIO.LOW)
    time.sleep(.1)
    print(str(datetime.datetime.now(datetime.timezone.utc).isoformat()) + ' High')
    GPIO.output(RPI3_GPIO_OUTPUT, GPIO.HIGH)

    time.sleep(.9)

GPIO.cleanup()
print("done")


