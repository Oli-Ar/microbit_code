from microbit import *
import time

# Dictionary storing the two images displayed by the program
pictures = {
    "counter_mode": Image("00900:"
                          "09990:"
                          "90909:"
                          "00900:"
                          "00900"),
    "timed_mode": Image("09990:"
                        "90909:"
                        "90909:"
                        "90099:"
                        "09990")
}


# Function to display a predefined image
def image_display(mode: bool):
    # Checks the current mode then displays an image based on it
    if mode:
        display.show(pictures['counter_mode'])
    else:
        display.show(pictures['timed_mode'])


# Function to check if the length of a value then display it
def display_string(value_to_display: str, loop: bool, wait: bool):
    if len(value_to_display) == 1:
        display.show(value_to_display)
    else:
        display.scroll(value_to_display, wait=wait, loop=loop)


# Function to be run on start up to handle what predefined image to display
# and to decide which will be run on a button press
def start_up():
    current_mode = True
    while True:
        image_display(current_mode)

        if button_b.is_pressed():
            current_mode = not current_mode
            image_display(current_mode)
            time.sleep(0.3)
        elif button_a.is_pressed():
            time.sleep(0.3)
            if current_mode:
                counter_mode(0)
            else:
                timer = Timer(60, 0)
                timer.start()


# Counter mode, counts up when the pins are triggered
def counter_mode(score: int):
    display_string(str(score), True, False)
    while True:
        if pin0.is_touched():
            score += 1
            display_string(str(score), True, False)
            pin1.write_digital(1)
            time.sleep(1)
            pin1.write_digital(0)
        if button_b.is_pressed():
            display_string(str(score), False, True)
            time.sleep(2)
            reset()


# Start of timer
class Timer:
    # Defines the values of the timer to count
    def __init__(self, input_time: int, score: int):
        self.current_time = input_time * 1000
        self.end_time = 0
        self.score = score

    # Function to start the timer and using arbitrary ticks count 60s
    def start(self):
        time_now = time.ticks_ms()
        self.end_time = time.ticks_add(time_now, self.current_time)
        while time.ticks_diff(self.end_time, time_now) > 0:
            disp = self.display_time(int(time.ticks_diff(self.end_time, time_now)) / 1000)
            display.show(disp)
            if button_a.is_pressed():
                self.current_time = time.ticks_diff(self.end_time, time.ticks_ms())
                time.sleep(0.3)
                paused = True
                while paused == True:
                    paused = self.pause()
            elif pin0.is_touched():
                self.score += 1
                pin1.write_digital(1)
                time.sleep(0.7)
                pin1.write_digital(0)
            time_now = time.ticks_ms()

        self.stop()

    # Function that will pause the timer
    def pause(self):
        display_string(str(self.score), False, False)
        while True:
            if button_a.is_pressed():
                time.sleep(0.3)
                self.end_time = time.ticks_add(self.current_time, time.ticks_ms())
                return False
            elif button_b.is_pressed():
                time.sleep(0.3)
                self.stop()

    # Function to stop timer and display score before returning to menu
    def stop(self):
        display_string(str(self.score), False, True)
        time.sleep(2)
        reset()

    @staticmethod  # Only called within class, displays the time left using whole screen to run semi-concurrently
    def display_time(time_diff):
        led_list = []
        for i in range(1, 26):
            if time_diff - (i * 2.4) >= 0:
                led_list.insert(0, str(9))
            else:
                led_list.insert(0, str(0))
        image_to_disp = Image(''.join(led_list[0:5]) + ":" +
                              ''.join(led_list[5:10]) + ":" +
                              ''.join(led_list[10:15]) + ":" +
                              ''.join(led_list[15:20]) + ":" +
                              ''.join(led_list[20:25]))
        return image_to_disp


start_up()