from engine import Engine
from transmission import Transmission
from wheel import Wheel


class Vehicle:
    def __init__(self):
        self.engine = Engine()
        self.transmission = Transmission()
        self.wheel = Wheel()

        self.current_gear = 1
        self.current_speed = 0.0
        self.current_engine_rpm = self.engine.min_rpm


if __name__ == "__main__":
    # Example usage
    vehicle = Vehicle()
    print("Vehicle initialized.")
