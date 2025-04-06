import math


class Wheel:
    def __init__(self, diameter_inches: float = 22.7):
        # copy the diameter_inches value to the instance variable
        self.__diameter_inches: float = diameter_inches

        # derive our circumference
        self.__circumference_inches = math.pi * self.__diameter_inches

        self.rpm_to_mph_ratio = self.__circumference_inches * 60 / 63360.0

    def get_diameter_inches(self) -> float:
        return self.__diameter_inches

    def speed_mph(self, input_rpm: float) -> float:
        return self.rpm_to_mph_ratio * input_rpm

    def rpm_from_speed(self, speed_mph: float) -> float:
        return speed_mph / self.rpm_to_mph_ratio


if __name__ == "__main__":
    # Example usage
    wheel = Wheel()
    print("Diameter in inches:", wheel.get_diameter_inches())

    for i in range(0, 1000, 100):
        print(
            f"Speed at {i} rpm: {wheel.speed_mph(i):.1f} mph",
        )

    for i in range(0, 100, 10):
        print(
            f"RPM at {i} mph: {int(wheel.rpm_from_speed(i))} rpm",
        )
