TCS_MODE_LINEAR = 1
TCS_MODE_QUADRATIC = 2


class TCS:
    # traction control system

    def __init__(
        self, slip_time: float = 0.5, min_grip: float = 0.0, mode: int = TCS_MODE_LINEAR
    ):
        self.slip_time = slip_time
        self.min_grip = min_grip
        self.mode = mode

    def grip_level(self, time: float = 0) -> float:

        if time <= 0:
            return self.min_grip

        if time >= self.slip_time:
            return 1.0

        grip_level = 0.0

        if self.mode == TCS_MODE_LINEAR:
            grip_level = self.min_grip + (1.0 - self.min_grip) * (time / self.slip_time)

        if self.mode == TCS_MODE_QUADRATIC:
            # self.min_grip + (1.0 - self.min_grip) * (time / self.slip_time)
            # y = −((𝑥−1)^2 )+1

            x = time / self.slip_time
            x = x - 1
            x = x * x
            y = -x + 1

            grip_level = self.min_grip + (1.0 - self.min_grip) * y

        return grip_level


def grip_report(t: TCS, time: float = 0) -> str:
    """
    Report the grip level of the TCS at a given time.
    """

    print(f"Grip level at {time:.2f} seconds: {t.grip_level(time):.2f}")


if __name__ == "__main__":
    linear_tcs = TCS()
    quadratic_tcs = TCS(min_grip=0.4, mode=TCS_MODE_QUADRATIC)

    for i in range(8):
        grip_report(linear_tcs, i * 0.1)

    for i in range(8):
        grip_report(quadratic_tcs, i * 0.1)
