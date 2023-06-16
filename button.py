import RPi.GPIO as GPIO
import time


class Button:
    def __init__(self, pin, double_press_interval=0.5):
        self.pin = pin
        self.prev_state = False
        self.double_press_interval = double_press_interval
        self.last_press_time = 0

        # Setup GPIO pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def is_button_pressed(self):
        state = GPIO.input(self.pin)
        if state == GPIO.LOW and not self.prev_state:
            current_time = time.time()
            time_since_last_press = current_time - self.last_press_time

            if time_since_last_press <= self.double_press_interval:
                self.last_press_time = 0  # Reset the last press time
                return "double_press"
            else:
                self.last_press_time = current_time

            self.prev_state = True
            return True
        elif state == GPIO.HIGH and self.prev_state:
            self.prev_state = False

        return False

    def cleanup(self):
        GPIO.cleanup(self.pin)
