import grpc
from concurrent import futures

import technics_42099_pb2_grpc as car_grpc
import technics_42099_pb2 as pb


class CarStatusService(car_grpc.CarStatusServicer):
    def GetBatteryInfo(self, request, context):
        return pb.BatteryStatus(voltage=7.0, current=0.1)

    def GetSteeringAngle(self, request, context):
        return pb.SteeringState(angle=0.0)


def serve_controller():
    controller = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    car_grpc.add_CarStatusServicer_to_server(CarStatusService(), controller)
    controller.add_insecure_port('0.0.0.0:50051')

    try:
        print("Starting service... ")
        controller.start()
        controller.wait_for_termination()
    except KeyboardInterrupt:
        print("Stopping service!")
        controller.stop(grace=True)


if __name__ == '__main__':
    serve_controller()