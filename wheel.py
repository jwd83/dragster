import math


class Wheel:
    def __init__(self, tire_spec: float | tuple = 22.7):

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


def wheel_report(wheel: Wheel) -> str:

    print("-" * 40)
    print("Diameter in inches:", wheel.get_diameter_inches())

    for i in range(0, 1000, 100):
        print(
            f"Speed at {i} rpm: {wheel.speed_mph(i):.1f} mph",
        )

    for i in range(0, 100, 10):
        print(
            f"RPM at {i} mph: {int(wheel.rpm_from_speed(i))} rpm",
        )


if __name__ == "__main__":
    # Example usage
    wheel = Wheel()
    wheel2 = Wheel((205, 55, 16))
    wheel3 = Wheel((335, 35, 17))

    wheel_report(wheel)

    wheel_report(wheel2)
    wheel_report(wheel3)
