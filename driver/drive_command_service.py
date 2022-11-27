import grpc

import technics_42099_pb2 as pb
import technics_42099_pb2_grpc as car_grpc


class DriveCommandService(car_grpc.DriveCommandServicer):

    def __init__(self):
        super(DriveCommandService, self).__init__()
        self.drive_data = {'motor': 0.0,  'steering_angle': 0.0}
        self.direction = 0
        self.is_braking = False

    def Drive(self, request: pb.DriveRequest, context):
        self.drive_data['motor'] = request.motor_speed
        self.drive_data['steering_angle'] = request.steering_angle
        self.direction = request.direction
        self.is_braking = request.is_braking
        # print(f"Want to drive to {self.drive_data['motor']} {self.drive_data['steering_angle']}")
        return pb.google_dot_protobuf_dot_empty__pb2.Empty()
