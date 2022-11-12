class InputDevice:
    def __init__(self) -> None:
        super().__init__()

    def listen(self) -> None:
        raise NotImplementedError()

    def throttle_level(self) -> int:
        raise NotImplementedError()

    def brake_level(self) -> int:
        raise NotImplementedError()

    def steer_angle(self) -> int:
        raise NotImplementedError()

    def direction(self) -> int:
        raise NotImplementedError()
