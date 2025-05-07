import math


class Wheel:
    def __init__(self, tire_spec: float | tuple = (185, 60, 14)):

        # check if we were provided a float or a tuple

        if isinstance(tire_spec, float):

            self.__diameter_inches: float = tire_spec

            # derive our circumference
            self.__circumference_inches = math.pi * self.__diameter_inches

            self.__rpm_to_mph_ratio = self.__circumference_inches * 60 / 63360.0

        elif isinstance(tire_spec, tuple):

            """
            tires use a measurement in the format of x/y/z
            example: 205/55/16

            x = tread width (mm)
            y = ratio
            z = wheel diameter (inches)

            if provided a tuple calculate tire diameter based on this

            """
            tire_tread_width_mm = tire_spec[0]
            tire_ratio = float(tire_spec[1]) / 100.0
            tire_wheel_diameter_in = tire_spec[2]

            tire_sidewall_mm = tire_ratio * tire_tread_width_mm
            tire_sidewall_in = tire_sidewall_mm / 25.4

            self.__diameter_inches: float = (
                2 * tire_sidewall_in + tire_wheel_diameter_in
            )

            # derive our circumference
            self.__circumference_inches = math.pi * self.__diameter_inches

            self.__rpm_to_mph_ratio = self.__circumference_inches * 60 / 63360.0

        # copy the diameter_inches value to the instance variable

    def get_diameter_inches(self) -> float:
        return self.__diameter_inches

    def speed_mph(self, input_rpm: float) -> float:
        return self.__rpm_to_mph_ratio * input_rpm

    def rpm_from_speed(self, speed_mph: float) -> float:
        return speed_mph / self.__rpm_to_mph_ratio


def wheel_report(wheel: Wheel, title: str | None = None) -> str:

    if title is None:
        title = "Unknown wheel"

    print("*" * 60)
    print(f"Wheel Report: {title}")

    print("-" * 40)
    print(f"Tire Diameter: {wheel.get_diameter_inches():.2f} in.")
    print("-" * 40)

    for i in range(0, 2000, 250):
        entry = f"Speed at {i} rpm"
        value = f"{wheel.speed_mph(i):.1f} MPH"
        print(f"{entry:<20} --> {value:>12}")
    print("-" * 40)

    for i in range(0, 200, 25):
        entry = f"Wheel RPM at {i} MPH"
        value = f"{wheel.rpm_from_speed(i):.1f} RPM"
        print(f"{entry:<22} --> {value:>12}")


if __name__ == "__main__":

    wheel_report(Wheel(), "AE86")
    wheel_report(Wheel((335, 35, 17)), "F40:Rear")
    wheel_report(Wheel((335, 30, 18)), "F50:Rear")
    wheel_report(Wheel((235, 40, 17)), "22B")
    wheel_report(Wheel((325, 30, 21)), "Valkyrie Rear")
    wheel_report(Wheel((235, 35, 19)), "RB17")
    wheel_report(Wheel((440, 60, 16)), "Funny/TopFuel:Rear")
    wheel_report(Wheel((405, 32, 18)), "F1:Rear")
