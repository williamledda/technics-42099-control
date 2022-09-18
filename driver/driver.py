import grpc
import asyncio
import threading
from concurrent import futures

import technics_42099_pb2_grpc as car_grpc
import technics_42099_pb2 as pb

from pybricksdev.connections.pybricks import PybricksHub
from pybricksdev.ble import find_device


voltage = 0.0
current = 0.0


class CarStatusService(car_grpc.CarStatusServicer):
    def GetBatteryInfo(self, request, context):
        return pb.BatteryStatus(voltage=voltage, current=current)

    def GetSteeringAngle(self, request, context):
        return pb.SteeringState(angle=0.0)


class MyBricksHub(PybricksHub):

    def __init__(self):
        super().__init__()

    def line_handler(self, line):
        global voltage
        global current

        super().line_handler(line)
        battery = line.decode().split()

        print(f'Line handler {line.decode()} -> {battery} ')

        voltage = float(battery[0])
        current = float(battery[1])

    async def run(self, py_path, wait=True, print_output=False):
        return await super().run(py_path, wait, print_output)


def driver_service():
    driver = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    car_grpc.add_CarStatusServicer_to_server(CarStatusService(), driver)
    driver.add_insecure_port('0.0.0.0:50051')

    try:
        print("Starting service... ")
        driver.start()
        driver.wait_for_termination()
    except KeyboardInterrupt:
        print("Stopping service!")
        driver.stop(grace=True)


async def hub_main():
    hub = MyBricksHub()
    print("Finding device...")
    dev = await find_device()

    print("Connecting to device...")
    await hub.connect(dev)
    print("Running device code...")
    await hub.run('onboard/hub.py', wait=False)

    for _ in range(30):
        await asyncio.sleep(1)

    await hub.disconnect()


if __name__ == '__main__':
    driver_srv = threading.Thread(target=driver_service)
    driver_srv.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(hub_main())

    driver_srv.join()

    print("Done...")
