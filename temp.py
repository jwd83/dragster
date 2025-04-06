import math


class Wheel:
    def __init__(self, diameter_inches: float = 22.7):
        # copy the diameter_inches value to the instance variable
        self.__diameter_inches: float = diameter_inches

        # derive our circumference
        self.__circumference_inches = math.pi * self.__diameter_inches

        self.__rpm_to_mph_ratio = self.__circumference_inches * 60 / 63360.0

    def get_diameter_inches(self) -> float:
        return self.__diameter_inches

    def speed_mph(self, input_rpm: float) -> float:
        return self.__rpm_to_mph_ratio * input_rpm

    def rpm_from_speed(self, speed_mph: float) -> float:
        return speed_mph / self.__rpm_to_mph_ratio


class Engine:

    def __init__(
        self,
        torque_curve: list = [
            (800, 20),
            (1000, 60),
            (2000, 105),
            (3000, 102),
            (4000, 100),
            (7000, 98),
            (8500, 44),
            (9000, 0),
        ],
    ):
        self.torque_curve = torque_curve.copy()
        self.max_rpm = max(torque[0] for torque in torque_curve)
        self.min_rpm = min(torque[0] for torque in torque_curve)
        self.max_torque = max(torque[1] for torque in torque_curve)
        self.max_horsepower = max(
            (torque[1] * torque[0]) / 5252 for torque in torque_curve
        )

    def torque(self, rpm: float):
        # Interpolate the torque value based on the RPM
        for i in range(len(self.torque_curve) - 1):
            if self.torque_curve[i][0] <= rpm <= self.torque_curve[i + 1][0]:
                rpm1, torque1 = self.torque_curve[i]
                rpm2, torque2 = self.torque_curve[i + 1]
                return torque1 + (torque2 - torque1) * (rpm - rpm1) / (rpm2 - rpm1)
        return 0.0

    def horsepower(self, rpm: float):
        # Calculate horsepower based on torque and RPM
        torque = self.torque(rpm)
        return (torque * rpm) / 5252


class Transmission:
    def __init__(
        self,
        forward_gears: list = [3.587, 2.022, 1.384, 1.0, 0.861],
        reverse_gear: float = 4.0,
        final_drive: float = 4.3,
    ):
        self.forward_gears = forward_gears.copy()
        self.reverse_gear = reverse_gear
        self.final_drive = final_drive
        self.max_gear = len(forward_gears)

    def output_rpm(self, input_rpm: float, gear: int) -> float:
        o_r = self.output_ratio(gear)
        return input_rpm * o_r

    def output_ratio(self, gear: int) -> float:
        ir = self.input_ratio(gear)
        if ir == 0.0:
            return 0.0
        return 1.0 / ir

    def input_rpm(self, output_rpm: float, gear: int) -> float:
        ir = self.input_ratio(gear)
        return output_rpm * ir

    def input_ratio(self, gear: int) -> float:
        return self.final_drive * self.gear_ratio(gear)

    def gear_ratio(self, gear: int) -> float:

        if gear == -1:
            return self.reverse_gear
        elif gear == 0:
            return 0.0
        elif 1 <= gear <= self.max_gear:
            return self.forward_gears[gear - 1]
        else:
            raise ValueError(
                f"Invalid gear: {gear}: int. Must be between -1 and {self.max_gear}."
            )

    def gear_name(self, gear: int) -> str:
        if gear == -1:
            return "R"
        elif gear == 0:
            return "N"
        elif 1 <= gear <= self.max_gear:
            return f"{gear}"
        else:
            raise ValueError(
                f"Invalid gear: {gear}: int. Must be between -1 and {self.max_gear}."
            )


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
        self.tick_rate = 1 / 60  # 60 FPS
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
            decel_modifier = 0.0
            accel_modifier = 0.0
            cur_mph = self.current_speed_mph

            decel_modifier = self.calculate_decel(cur_mph, self.tick_rate)

            self.current_speed_mph = max(0, cur_mph + accel_modifier + decel_modifier)

            self.current_engine_rpm = self.engine_rpm_from_speed_and_gear()

    def calculate_decel(
        self,
        input_velocity_mph,
        dt,
    ):
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
        iv = input_velocity_mph * 0.44704  # Convert mph to m/s
        g = 9.81  # m/s^2 (gravity)
        Cd = self.drag_coefficient
        FrA = self.frontal_area
        Crr = self.rolling_resistance

        # formulas
        F_rr = Crr * mass * g
        F_drag = 0.5 * Ad * Cd * FrA * iv**2
        F_total = F_rr + F_drag
        a = -F_total / mass
        dv = a * dt
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

    vehicle = Vehicle()

    vehicle.current_gear = 5
    vehicle.current_engine_rpm = 6000

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
