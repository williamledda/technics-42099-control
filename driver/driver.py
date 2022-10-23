import grpc
import asyncio
import threading
from concurrent import futures

import drive_command_service as drive

import technics_42099_pb2 as pb
import technics_42099_pb2_grpc as car_grpc

from pybricksdev.ble import find_device
from pybricksdev.connections.pybricks import PybricksHub


status = {
    'battery': {'voltage': 0.0, 'current': 0.0},
    'tilt': {'pitch': 0.0, 'roll': 0.0},
    'w': [0.0, 0.0, 0.0],
    'acc': [0.0, 0.0, 0.0]
}

stop = False
drive_grpc_service = drive.DriveCommandService()


class CarStatusService(car_grpc.CarStatusServicer):
    def GetBatteryInfo(self, request, context):
        return pb.BatteryStatus(voltage=status['battery']['voltage'],
                                current=status['battery']['current'])

    def GetIMUData(self, request, context):
        return pb.IMUStatus(pitch=status['tilt']['pitch'],
                            roll=status['tilt']['roll'],
                            angular_velocity=status['w'],
                            acceleration=status['acc'])

    def GetSteeringAngle(self, request, context):
        return pb.SteeringState(angle=0.0)


class MyBricksHub(PybricksHub):

    def __init__(self):
        super(MyBricksHub, self).__init__()

    def line_handler(self, line):
        global status

        super(MyBricksHub, self).line_handler(line)

        line_str = line.decode()

        if line_str and len(line_str) > 2 and line_str.startswith('$') and line_str.endswith('$'):
            status_line = line_str[1:len(line_str)-1].split(',')

            # print(f'Line handler {line_str} -> {status_line} ')

            status['battery']['voltage'] = float(status_line[0])
            status['battery']['current'] = float(status_line[1])
            status['tilt']['pitch'] = float(status_line[2])
            status['tilt']['roll'] = float(status_line[3])
            status['w'] = [float(status_line[4]), float(status_line[5]), float(status_line[6])]
            status['acc'] = [float(status_line[7]), float(status_line[8]), float(status_line[9])]

    async def run(self, py_path, wait=True, print_output=False):
        return await super(MyBricksHub, self).run(py_path, wait, print_output)


def status_service():
    status_srv = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    car_grpc.add_CarStatusServicer_to_server(CarStatusService(), status_srv)
    status_srv.add_insecure_port('0.0.0.0:50051')

    try:
        print("Starting car status service... ")
        status_srv.start()
        status_srv.wait_for_termination()
    except KeyboardInterrupt:
        print("Stopping service!")
        status_srv.stop(grace=True)


def drive_service():
    global drive_grpc_service

    drive_srv = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    car_grpc.add_DriveCommandServicer_to_server(drive_grpc_service, drive_srv)
    drive_srv.add_insecure_port('0.0.0.0:50052')

    try:
        print("Starting driving command service...\n")
        drive_srv.start()
        drive_srv.wait_for_termination()
    except KeyboardInterrupt:
        print("Stopping service!\n")
        drive_srv.stop(grace=True)


async def hub_main():
    hub = MyBricksHub()
    print("Finding device...")
    dev = await find_device()

    print("Connecting to device...")
    await hub.connect(dev)
    print("Running device code...")
    await hub.run('onboard/hub.py', wait=False)

    while not stop:
        # print(f"Command from grpc: {drive_grpc_service.drive_data['motor']} "
        #       f"{drive_grpc_service.drive_data['steering_angle']}")
        drive_cmd = f"d:{drive_grpc_service.drive_data['motor']}:{drive_grpc_service.drive_data['steering_angle']};"
        await hub.write(drive_cmd.encode())
        await asyncio.sleep(0.2)

    await hub.write(b"s:;")

    await hub.disconnect()


if __name__ == '__main__':
    status_th = threading.Thread(target=status_service)
    status_th.start()

    drive_cmd_th = threading.Thread(target=drive_service)
    drive_cmd_th.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(hub_main())

    status_th.join()
    drive_cmd_th.join()

    print("Done...")
