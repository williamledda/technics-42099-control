from pyPS4Controller.controller import Controller


class PS4Controller(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)
        self.DRIVE_RESOLUTION = 1000 / (32767 * 2)
        self.STEER_RESOLUTION = 90 / 32767
        self.drive_cmd = {'throttle': 0.0, 'brake': 0.0, 'steer': 0.0}

    def compute_drive_tgt(self, value: float) -> float:
        return int(value * self.DRIVE_RESOLUTION)

    def compute_steer_tgt(self, value: float) -> float:
        return int(value * self.STEER_RESOLUTION)

    # Acceleration...
    def on_R2_press(self, value: float) -> None:
        self.drive_cmd['throttle'] = self.compute_drive_tgt(value + 32767)
        print(f"Throttle {value} -> {self.drive_cmd['throttle']}")

    def on_L2_press(self, value: float) -> None:
        self.drive_cmd['brake'] = self.compute_drive_tgt(value + 32767)
        print(f"Brakes {value} -> {self.drive_cmd['brake']}")

    def on_L2_release(self):
        print("Stop braking")

    def on_R2_release(self):
        print("Stop throttle")

    def on_L3_left(self, value):
        self.drive_cmd['steer'] = self.compute_steer_tgt(value)
        print(f"Steering left: {value} -> {self.drive_cmd['steer']}")

    def on_L3_right(self, value):
        self.drive_cmd['steer'] = self.compute_steer_tgt(value)
        print(f"Steering right: {value} -> {self.drive_cmd['steer']}")

    def on_R3_left(self, value):
        pass

    def on_R3_right(self, value):
        pass

    def on_L3_y_at_rest(self):
        print("on_L3_y_at_rest")
        pass

    def on_L3_x_at_rest(self):
        print("on_L3_x_at_rest")

    def on_R3_x_at_rest(self):
        pass

    def on_R3_y_at_rest(self):
        pass

    def on_x_press(self):
        pass

    def on_x_release(self):
        pass

    def on_triangle_press(self):
        pass

    def on_triangle_release(self):
        pass

    def on_circle_press(self):
        pass

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

    # def start_recording(self):
    #     now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    #     self.camera = picamera.PiCamera()
    #     self.camera.resolution = (640, 480)
    #     self.camera.start_recording('../../video/recording_{}.h264'.format(now))
    #     self.camera.wait_recording(1)
    #
    # def stop_recording(self):
    #     self.camera.stop_recording()
    #     self.camera.close()
    #     self.camera = None

    # def on_circle_press(self):
    #     if self.camera is None:
    #         print("Start recording...")
    #         self.start_recording()
    #         self.led.colorWipe(self.led.strip, Color(64, 0, 0))
    #         print("Video recording started")
    #     else:
    #         print('Stop recording...')
    #         self.stop_recording()
    #         self.led.colorWipe(self.led.strip, Color(0, 0, 0))
    #         print("Video recording stopped")

# def read_input(controller):
#     controller.listen()


if __name__ == "__main__":
    ps4_controller = PS4Controller(interface="/dev/input/js0", connecting_using_ds4drv=False)

    try:
        ps4_controller.listen()
    except KeyboardInterrupt:
        print("Done!")



    # input_thread = threading.Thread(target=read_input, args=(ps4_controller,))
    # input_thread.start()
    # ALPHA = (1 / 2.0)
    # DAMP = (1 - ALPHA)
    # out_speed = [0, 0, 0, 0]
    # motor_data = open('../../log/motor.csv', 'w', newline='')
    # motor_csv = csv.writer(motor_data, delimiter=',')
    #
    # motor_csv.writerow(['tgt_front_left', 'tgt_rear_left', 'tgt_front_right', 'tgt_rear_right',
    #                     'out_front_left', 'out_rear_left', 'out_front_right', 'out_rear_right'])

    # led = Led()
    #
    # print("Testing leds...")
    # led.colorWipe(led.strip, Color(64, 64, 64))
    # time.sleep(1.0)
    # led.colorWipe(led.strip, Color(0, 0, 0))
    # print("Testing leds end...")


    # while True:
    #     try:
    #         for i in range(0, 4):
    #             out_speed[i] = int((ALPHA * ps4_controller.tgt_speed[i]) + (DAMP * out_speed[i]))
    #             if abs(out_speed[i]) < 300:
    #                 out_speed[i] = 0
    #
    #         motor.setMotorModel(out_speed[0], out_speed[1], out_speed[2], out_speed[3])
    #         motor_csv.writerow([ps4_controller.tgt_speed[0], ps4_controller.tgt_speed[1],
    #                             ps4_controller.tgt_speed[2], ps4_controller.tgt_speed[3],
    #                             out_speed[0], out_speed[1], out_speed[2], out_speed[3]])
    #
    #         # print("{},{},{},{},{},{},{},{}".format(
    #         #    ps4_controller.tgt_speed[0], ps4_controller.tgt_speed[1],
    #         #    ps4_controller.tgt_speed[2], ps4_controller.tgt_speed[3],
    #         #    out_speed[0], out_speed[1], out_speed[2], out_speed[3]), flush=True)
    #         time.sleep(0.02)  # 20 Hz rate
    #     except KeyboardInterrupt:
    #         motor.setMotorModel(0, 0, 0, 0)
    #         break
    #
    # # print("Closing input thread")
    #
    # try:
    #     stop_thread(input_thread)
    # except:
    #     pass