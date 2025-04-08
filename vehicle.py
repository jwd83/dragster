from engine import Engine
from transmission import Transmission
from wheel import Wheel


class Vehicle:
    def __init__(self):
        self.engine = Engine()
        self.transmission = Transmission()
        self.wheel = Wheel()
        self.weight: float = 900.0  # kg
        self.ticks: int = 0
        self.current_gear: int = 1
        self.current_speed_mph = 0.0
        self.current_engine_rpm = self.engine.min_rpm
        self.current_throttle = 0.0
        self.tick_rate = 1 / 60  # simulation rate (Hz)
        self.drag_coefficient = 0.3
        self.rolling_resistance = 0.015
        self.frontal_area = 2.0  # m^2
        self.air_density = 1.225  # kg/m^3

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
            diff = self.calculate_acceleration()
            diff += self.calculate_deceleration()
            self.current_speed_mph += diff

            self.current_speed_mph = max(0, self.current_speed_mph)

            self.current_engine_rpm = self.engine_rpm_from_speed_and_gear()

    def calculate_acceleration(self) -> float:
        if self.current_throttle == 0 or self.current_speed_mph == 0:
            return 0.0

        # Get engine power at current RPM (throttle-modulated)
        hp = self.engine.horsepower(self.current_engine_rpm) * self.current_throttle

        # Convert horsepower to watts (1 hp = 745.7 watts)
        power_watts = hp * 745.7

        # Convert speed to m/s for force = power / velocity
        speed_mps = self.current_speed_mph * 0.44704

        # Avoid division by zero at very low speeds
        if speed_mps < 0.1:
            speed_mps = 0.1

        # Compute force at wheels
        force = power_watts / speed_mps

        # Estimate drivetrain efficiency losses (~85%)
        drivetrain_efficiency = 0.85
        force *= drivetrain_efficiency

        # Compute acceleration (a = F / m)
        acceleration_mps2 = force / self.weight

        # Convert m/s² to mph per tick
        acceleration_mph = acceleration_mps2 * self.tick_rate * 2.23694

        return acceleration_mph

    def calculate_deceleration(self) -> float:
        """
        Calculates the new speed of a coasting vehicle over a time step.

        Parameters:
            input_velocity_mph (float): Current speed in mph
            dt (float): Time step in seconds (e.g., 0.02s for 50 Hz)

        Returns:
            dv (float): Change in speed over the time step (will be negative or zero)
        """
        # unit conversions
        mass = self.weight  # kg
        Ad = 1.225  # kg/m^3 (standard air density at sea level)
        iv = self.current_throttle * 0.44704  # Convert mph to m/s
        g = 9.81  # m/s^2 (gravity)
        Cd = self.drag_coefficient
        FrA = self.frontal_area
        Crr = self.rolling_resistance

        # formulas
        F_rr = Crr * mass * g
        F_drag = 0.5 * Ad * Cd * FrA * iv**2
        F_total = F_rr + F_drag
        a = -F_total / mass
        dv = a * self.tick_rate
        dv = dv * 2.23694  # Convert m/s to mph
        return dv

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
    vehicle.current_engine_rpm = 850

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
    # vehicle.current_throttle = 1  # No throttle
    vehicle.update()

    print(vehicle.readout())

    print("...")
    while vehicle.current_speed_mph > 0 and vehicle.current_speed_mph < 30:

        if vehicle.ticks % 500 == 0:
            print(vehicle.readout())
        vehicle.update()
    print(vehicle.readout())
