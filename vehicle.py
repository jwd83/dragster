from engine import Engine
from transmission import Transmission
from wheel import Wheel


class Vehicle:
    def __init__(self):
        self.engine = Engine()
        self.transmission = Transmission()
        self.wheel = Wheel()
        self.weight = 2000
        self.ticks: int = 0
        self.current_gear = 1
        self.current_speed_mph = 0.0
        self.current_engine_rpm = self.engine.min_rpm
        self.current_throttle = 0.0
        self.tick_rate = 1 / 60  # 60 FPS
        self.drag_coefficient = 0.3
        self.rolling_resistance = 0.5
        self.air_density = 1

    def readout(self) -> str:
        return f"Gear: {self.current_gear}, Speed: {self.current_speed_mph:.2f} mph, TPS: {self.current_throttle:.2f} RPM: {self.current_engine_rpm:.2f}, Ticks: {self.ticks} ({self.ticks * self.tick_rate:.4f} sec)"

    def update(self):
        self.ticks += 1

        # if the vehicle is not moving, accelerate it to the idle speed instantly to get moving
        if self.current_speed_mph == 0:
            if self.current_throttle > 0:
                # print("Clutch engaged, velocity set via engine speed and gear.")
                self.current_speed_mph = self.speed_mph_from_engine_rpm_and_gear()
        else:
            # if the vehicle is moving and there is no throttle, decelerate it to 0
            decel_modifier = 0.0
            accel_modifier = 0.0

            # determinte decel modifier based on drag and rolling resistance
            drag_force = (
                self.drag_coefficient * self.air_density * (self.current_speed_mph**2)
            )
            rolling_resistance_force = self.rolling_resistance * self.weight
            decel_modifier = (drag_force + rolling_resistance_force) / self.weight
            decel_modifier *= self.tick_rate
            decel_modifier = min(decel_modifier, self.current_speed_mph)

            self.current_speed_mph += accel_modifier - decel_modifier

            self.current_engine_rpm = self.engine_rpm_from_speed_and_gear()

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

    vehicle.current_gear = 1
    vehicle.current_engine_rpm = 1000

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

    # engage the clutch to start the vehicle moving
    vehicle.current_throttle = 1.0  # Full throttle
    vehicle.update()
    print(vehicle.readout())
    vehicle.current_throttle = 0.0  # No throttle
    vehicle.update()

    print(vehicle.readout())

    print("...")
    while vehicle.current_speed_mph > 0:
        vehicle.update()
    print(vehicle.readout())
