from engine import Engine
from transmission import Transmission
from wheel import Wheel


class Vehicle:
    def __init__(self):
        self.engine = Engine()
        self.transmission = Transmission()
        self.wheel = Wheel()


if __name__ == "__main__":
    # Example usage
    vehicle = Vehicle()
    print("Vehicle initialized.")
