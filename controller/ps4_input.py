from pyPS4Controller.controller import Controller
from input_device import InputDevice


class PS4Controller(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.DRIVE_RESOLUTION = 100 / (32767 * 2)
        self.STEER_RESOLUTION = 90 / 32767
        self.drive_cmd = {'throttle': 0, 'brake': 0, 'steer': 0}
        self.direction = 0

    def compute_drive_tgt(self, value: float) -> int:
        return int(value * self.DRIVE_RESOLUTION)

    def compute_steer_tgt(self, value: float) -> int:
        return int(value * self.STEER_RESOLUTION)

    # Acceleration...
    def on_R2_press(self, value: float) -> None:
        self.drive_cmd['throttle'] = self.compute_drive_tgt(value + 32767)
        # print(f"Throttle {value} -> {self.drive_cmd['throttle']}")

    def on_L2_press(self, value: float) -> None:
        self.drive_cmd['brake'] = self.compute_drive_tgt(value + 32767)
        # print(f"Brakes {value} -> {self.drive_cmd['brake']}")

    def on_L2_release(self):
        self.drive_cmd['brake'] = 0
        # print("Stop braking")

    def on_R2_release(self):
        self.drive_cmd['throttle'] = 0
        # print("Stop throttle")

    def on_L3_left(self, value):
        self.drive_cmd['steer'] = self.compute_steer_tgt(value)
        # print(f"Steering left: {value} -> {self.drive_cmd['steer']}")

    def on_L3_right(self, value):
        self.drive_cmd['steer'] = self.compute_steer_tgt(value)
        # print(f"Steering right: {value} -> {self.drive_cmd['steer']}")

    def on_R3_left(self, value):
        pass

    def on_R3_right(self, value):
        pass

    def on_L3_y_at_rest(self):
        self.drive_cmd['steer'] = 0
        pass

    def on_L3_x_at_rest(self):
        self.drive_cmd['steer'] = 0

    def on_R3_x_at_rest(self):
        pass

    def on_R3_y_at_rest(self):
        pass

    def on_x_press(self):
        self.direction = -1
        # print("Reverse")

    def on_x_release(self):
        pass

    def on_triangle_press(self):
        self.direction = 1
        # print("Forward")

    def on_triangle_release(self):
        pass

    def on_circle_press(self):
        self.direction = 0
        # print("Neutral")

    def on_circle_release(self):
        pass

    def on_square_press(self):
        pass

    def on_square_release(self):
        pass

    def on_L1_press(self):
        pass

    def on_L1_release(self):
        pass

    def on_R1_press(self):
        pass

    def on_R1_release(self):
        pass

    def on_up_arrow_press(self):
        pass

    def on_up_down_arrow_release(self):
        pass

    def on_down_arrow_press(self):
        pass

    def on_left_arrow_press(self):
        pass

    def on_left_right_arrow_release(self):
        pass

    def on_right_arrow_press(self):
        pass

    def on_L3_up(self, value):
        pass

    def on_L3_down(self, value):
        pass

    def on_L3_press(self):
        pass

    def on_L3_release(self):
        pass

    def on_R3_up(self, value):
        pass

    def on_R3_down(self, value):
        pass

    def on_R3_press(self):
        pass

    def on_R3_release(self):
        pass

    def on_options_press(self):
        pass

    def on_options_release(self):
        pass

    def on_share_press(self):
        pass

    def on_share_release(self):
        pass

    def on_playstation_button_press(self):
        pass

    def on_playstation_button_release(self):
        pass


class PS4Input(InputDevice):

    def __init__(self) -> None:
        super(InputDevice, self).__init__()
        self.ps4 = PS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)

    def listen(self) -> None:
        self.ps4.listen()

    def throttle_level(self) -> int:
        return self.ps4.drive_cmd["throttle"]

    def brake_level(self) -> int:
        return self.ps4.drive_cmd["brake"]

    def steer_angle(self) -> int:
        return self.ps4.drive_cmd["steer"]

    def direction(self) -> int:
        return self.ps4.direction


if __name__ == "__main__":
    ps4_controller = PS4Input()
    try:
        ps4_controller.listen()
    except KeyboardInterrupt:
        print("Done!")
