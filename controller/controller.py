import grpc
import time
import threading

import technics_42099_pb2 as pb
import technics_42099_pb2_grpc as car_grpc
from input import InputDevice, PS4Input

empty = pb.google_dot_protobuf_dot_empty__pb2.Empty()
stop = False


def status_loop() -> None:
    with grpc.insecure_channel('192.168.0.31:50051') as status_channel:
        global stop
        car_service_stub = car_grpc.CarStatusStub(status_channel)

        while not stop:
            response = car_service_stub.GetBatteryInfo(empty)
            print(f"Car status      : {response.voltage}V {response.current}A")

            response = car_service_stub.GetIMUData(empty)
            print(f"Pitch, Roll     : {response.pitch}rad {response.roll}rad")
            print(f"Angular velocity: {response.angular_velocity} rad/s")
            print(f"Acceleration    : {response.acceleration} rad/s²")
            time.sleep(1.0)


def run(input_device: InputDevice) -> None:
    global stop
    status_th = threading.Thread(target=status_loop)
    drive_channel = grpc.insecure_channel('192.168.0.31:50052')
    drive_command_stub = car_grpc.DriveCommandStub(drive_channel)

    status_th.start()

    while not stop:
        # print(f"PS4 drive command: {ps4_input.throttle_level()} {ps4_input.brake_level()} "
        #       f"{ps4_input.steer_angle()} {ps4_input.direction()}")
        drive_speed = (input_device.throttle_level() - input_device.brake_level()) * 10

        drive_speed = max(0, drive_speed) * input_device.direction()

        drive_command_stub.Drive(pb.DriveRequest(motor_speed=drive_speed,
                                                 steering_angle=input_device.steer_angle(),
                                                 direction=input_device.direction(),
                                                 is_braking=(input_device.brake_level() > 0)))
        time.sleep(0.05)

    status_th.join()


def read_input(dev: InputDevice) -> None:
    dev.listen()


if __name__ == '__main__':
    try:
        ps4_controller = PS4Input()
        input_thread = threading.Thread(target=read_input, args=(ps4_controller,))
        input_thread.start()
        run(ps4_controller)
    except KeyboardInterrupt:
        stop = True
        print("Closing service")
