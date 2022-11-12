from usys import stdin
from uselect import poll
from pybricks.hubs import TechnicHub
from pybricks.tools import wait, StopWatch

from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction, Stop, Color

hub = TechnicHub()
command_buffer = ""
running = True


class MotorControl:
    def __init__(self):
        # Initialize the motors
        self.limit = 0.0
        self.steer = Motor(Port.C)
        self.front = Motor(Port.A, Direction.COUNTERCLOCKWISE)
        self.rear = Motor(Port.B, Direction.COUNTERCLOCKWISE)
        hub.light.off()

    def init_motors(self):
        # Lower the acceleration so the car starts and stops realistically.
        self.front.control.limits(acceleration=1000)
        self.rear.control.limits(acceleration=1000)

        # Find the steering endpoint on the left and right. The difference
        # between them is the total angle it takes to go from left to right.
        # The middle is in between.
        left_end = self.steer.run_until_stalled(-200, then=Stop.HOLD)
        right_end = self.steer.run_until_stalled(200, then=Stop.HOLD)

        # We are now at the right limit. We reset the motor angle to the
        # limit value, so that the angle is 0 when the steering mechanism is
        # centered.
        self.limit = (right_end - left_end) // 2
        self.steer.reset_angle(self.limit)
        self.steer.run_target(speed=200, target_angle=0, then=Stop.COAST)

    # Given a motor speed (deg/s) and a steering motor angle (deg), this
    # function makes the car move at the desired speed and turn angle.
    # The car keeps moving until you give another drive command.
    def drive(self, drive_motor_speed, steer_angle):
        # Start running the drive motors
        self.front.run(drive_motor_speed)
        self.rear.run(drive_motor_speed)

        # Limit the steering value for safety, and then start the steer
        # motor.
        limited_angle = max(-self.limit, min(steer_angle, self.limit))
        self.steer.run_target(200, limited_angle, wait=False)


def try_wait(time):
    timer = StopWatch()
    while timer.time() < time:
        yield


def status_task():
    while True:
        yield from try_wait(1000)
        voltage = hub.battery.voltage()
        current = hub.battery.current()
        pitch, roll = hub.imu.tilt()
        velocity = hub.imu.angular_velocity()
        acc = hub.imu.acceleration()
        print('${},{},{},{},{},{},{},{},{},{}$'.format((voltage / 1000), (current / 1000), pitch, roll, velocity[0],
                                                       velocity[1], velocity[2], acc[0], acc[1], acc[2]))


def input_handler(command):
    global running
    # Obtain the list of commands
    command_list = command.split(':')

    if command_list[0] == "s":
        # Stop
        running = False
    elif command_list[0] == "d":
        # drive
        # Get motor speed and steering angle
        motor_speed = float(command_list[1])
        steer_angle = float(command_list[2])

        # Set driving speed and steering angle
        # print("Driving speed: {} Steering angle: {}".format(motor_speed, steer_angle))
        motor_control.drive(motor_speed, steer_angle)
        if motor_speed < 0:
            hub.light.on(Color.WHITE)
        elif motor_speed == 0:
            hub.light.off()
        else:
            hub.light.blink(Color.GREEN, [100, 50])


def update_input(char):
    global command_buffer
    if char == ";":
        input_handler(command_buffer)
        command_buffer = ""
    else:
        command_buffer += char


def read_command_task():
    loop_poll = poll()
    loop_poll.register(stdin)

    while True:
        while loop_poll.poll(1):  # times out after 100ms
            char = stdin.read(1)
            if char is not None:
                update_input(char)

        yield from try_wait(100)


def main_loop():
    # each "task" will run until the first yield statement here
    tasks = [read_command_task(), status_task()]

    while running:
        # Warning! This assumes that all tasks in the list run forever.
        # If they don't, we will eventually get an unhandled StopIteration exception.
        for t in tasks:
            next(t)

        # Give the CPU some time to relax (this is especially important on EV3)
        wait(1)


motor_control = MotorControl()
motor_control.init_motors()
main_loop()
