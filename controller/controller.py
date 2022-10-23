import grpc
import time
import threading

import technics_42099_pb2 as pb
import technics_42099_pb2_grpc as car_grpc

empty = pb.google_dot_protobuf_dot_empty__pb2.Empty()
stop = False


def status_loop():
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


def run():
    global stop
    status_th = threading.Thread(target=status_loop)
    drive_channel = grpc.insecure_channel('192.168.0.31:50052')
    drive_command_stub = car_grpc.DriveCommandStub(drive_channel)

    status_th.start()

    drive_command_stub.Drive(pb.DriveRequest(motor_speed=500, steering_angle=0))
    time.sleep(2.0)
    drive_command_stub.Drive(pb.DriveRequest(motor_speed=-500, steering_angle=0))
    time.sleep(2.0)
    drive_command_stub.Drive(pb.DriveRequest(motor_speed=500, steering_angle=50))
    time.sleep(2.0)
    drive_command_stub.Drive(pb.DriveRequest(motor_speed=-500, steering_angle=0))
    time.sleep(2.0)
    drive_command_stub.Drive(pb.DriveRequest(motor_speed=500, steering_angle=-50))
    time.sleep(2.0)
    drive_command_stub.Drive(pb.DriveRequest(motor_speed=-500, steering_angle=0))
    time.sleep(2.0)
    drive_command_stub.Drive(pb.DriveRequest(motor_speed=0, steering_angle=0))
    time.sleep(2.0)

    status_th.join()


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        stop = True
        print("Closing service")
