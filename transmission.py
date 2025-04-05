# gear_selection is defined as an integer: 0 for neutral, -1 for reverse, and 1 through max_gear for forward gears


class Transmission:
    def __init__(self, forward_gears: list, reverse_gear: float, final_drive: float):
        self.forward_gears = forward_gears.copy()
        self.reverse_gear = reverse_gear
        self.final_drive = final_drive
        self.max_gear = len(forward_gears)

    def output_rpm(self, input_rpm: float, gear: int) -> float:
        pass

    def output_ratio(self, gear: int) -> float:
        pass

    def input_rpm(self, output_rpm: float, gear: int) -> float:
        pass

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
