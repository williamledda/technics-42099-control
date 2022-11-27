import grpc

from fastapi import FastAPI

import technics_42099_pb2 as pb
import technics_42099_pb2_grpc as car_grpc

app = FastAPI()
status_ch = grpc.insecure_channel('192.168.0.31:50051')
status_srv = car_grpc.CarStatusStub(status_ch)
empty = pb.google_dot_protobuf_dot_empty__pb2.Empty()


@app.get("/battery")
def read_battery():
    response = status_srv.GetBatteryInfo(empty)
    return {"voltage: ": response.voltage,
            "current": response.current}


@app.get("/imu")
def read_tilt():
    response = status_srv.GetIMUData(empty)
    print(f"Pitch, Roll     : {response.pitch}rad {response.roll}rad")
    print(f"Angular velocity: {response.angular_velocity} rad/s")
    print(f"Acceleration    : {response.acceleration} rad/s²")

    return {"pitch": response.pitch,
            "roll": response.roll,
            "w": list(response.angular_velocity),
            "acc": list(response.acceleration)
            }

