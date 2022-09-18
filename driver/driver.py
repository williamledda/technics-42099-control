import grpc
import time

import technics_42099_pb2_grpc as car_grpc
import technics_42099_pb2 as pb


def run():
    empty = pb.google_dot_protobuf_dot_empty__pb2.Empty()
    with grpc.insecure_channel('192.168.0.32:50051') as channel:
        car_service_stub = car_grpc.CarStatusStub(channel)
        while True:
            response = car_service_stub.GetBatteryInfo(empty)
            print(f"Car status: {response.voltage}V {response.current}A")
            time.sleep(1.0)


if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt:
        print("Closing service")