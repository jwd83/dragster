from engine import Engine
from transmission import Transmission
from wheel import Wheel


class Vehicle:
    def __init__(self):
        self.engine = Engine()
        self.transmission = Transmission()
        self.wheel = Wheel()
        self.weight = 2000

        self.current_gear = 1
        self.current_speed_mph = 0.0
        self.current_engine_rpm = self.engine.min_rpm
        self.current_throttle = 0.0

    def readout(self) -> str:
        return f"Gear: {self.current_gear}, Speed: {self.current_speed_mph:.2f} mph, RPM: {self.current_engine_rpm:.2f}"

    def update(self):
        tick: float = 1 / 60

        # if the vehicle is not moving, accelerate it to the idle speed instantly to get moving
        if self.current_speed_mph == 0:
            if self.current_throttle > 0:
                self.current_speed_mph = self.speed_mph_from_engine_rpm_and_gear()
        else:
            # if the vehicle is currently moving calculate the acceleration
            self.current_speed_mph += tick

    def engine_rpm_from_speed_and_gear(self) -> float:
        # Calculate the engine RPM based on the current speed and gear
        wheel_rpm = self.wheel.rpm_from_speed(self.current_speed_mph)
        return self.transmission.input_rpm(wheel_rpm, self.current_gear)

    def speed_mph_from_engine_rpm_and_gear(self) -> float:

        wheel_rpm = self.transmission.output_rpm(
            self.current_engine_rpm, self.current_gear
        )
        return self.wheel.speed_mph(wheel_rpm)


if __name__ == "__main__":
    # Example usage
    vehicle = Vehicle()
    print("Vehicle initialized.")

    print("Current speed:", vehicle.current_speed_mph, "mph")
    print("Current gear:", vehicle.current_gear)
    print("Current engine RPM:", vehicle.current_engine_rpm)

    print("Engine RPM from speed and gear:", vehicle.engine_rpm_from_speed_and_gear())
    print(
        "Speed from engine RPM and gear:", vehicle.speed_mph_from_engine_rpm_and_gear()
    )

    # starting sim
    print("-" * 80)
    print("Starting simulation...")
    print("-" * 80)
    vehicle.update()
    print(vehicle.readout())

    vehicle.current_throttle = 1.0  # Full throttle

    for i in range(10):
        vehicle.update()
        print(vehicle.readout())
