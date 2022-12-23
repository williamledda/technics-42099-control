#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

TrackPin = 8
stop_loop = False
current_level = None
start_time = float()
stop_time = float()


def measure(event):
	global start_time
	global stop_time

	if GPIO.input(TrackPin) == GPIO.HIGH:
		print(f"Measure started")
		start_time = time.perf_counter()
	else:
		stop_time = time.perf_counter()
		dt = stop_time - start_time
		print(f"Time elapsed: {dt} - > Estimated speed: {0.297 / dt} m/s")


def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	GPIO.setup(TrackPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.add_event_detect(TrackPin, GPIO.BOTH, callback=measure)


def loop():
	timestamp = str(time.time()).split('.')[0]
	file_name = f"raw_{timestamp}.log"
	f = open(file_name, "a")
	f.write(f"raw_{timestamp}\n")

	while not stop_loop:
		lvl = GPIO.input(TrackPin)

		f.write(f"{lvl}\n")
		time.sleep(0.05)

	f.close()


def destroy():
	GPIO.cleanup()                     # Release resource


if __name__ == '__main__':     # Program start from here
	setup()
	current_level = GPIO.input(TrackPin)
	try:
		loop()
	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		stop = True
		destroy()
