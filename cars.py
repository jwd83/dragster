"""

Cars are named after birds of colors that they resemble.

econobox - puffin (black and white)
rally car - blue jay (blue)
sport car - goldfinch (yellow) 460hp, 2500lb
supercar - cardinal (red) 475hp 2400lb
formula - red-headed woodpecker (red and white)
funny - painted bunting (red and blue)
top fuel - common grackle (black and green)


"""

from vehicle import Vehicle
from engine import Engine
from transmission import Transmission
from wheel import Wheel


def puffin() -> Vehicle:

    return Vehicle()


def blue_jay() -> Vehicle:

    return Vehicle(
        Engine(
            [
                (1000, 80),
                (2000, 120),
                (3000, 240),
                (3800, 370),
                (4100, 350),
                (6600, 330),
                (6800, 310),
                (6950, 11),
                (7000, 0),
            ],
            shift_rpm=6800,
            launch_rpm=2400,
        ),
        weight_lbs=2800,
    )


def painted_bunting() -> Vehicle:

    return Vehicle(
        Engine(
            [(1000, 3000), (5000, 2000), (5500, 0)],
            shift_rpm=5000,
        ),
        Transmission(
            forward_gears=[3.6, 1.8, 1.4, 1],
            reverse_gear=0.4,
            final_drive=2.4,
        ),
        Wheel(50.0),
        weight_lbs=2300,
    )


def cardinal() -> Vehicle:

    return Vehicle(
        Engine(
            [
                (1000, 100),
                (2000, 200),
                (2500, 300),
                (4000, 440),
                (5252, 450),
                (6000, 420),
                (6500, 399),
                (6750, 300),
                (7000, 0),
            ],
            shift_rpm=6500,
            launch_rpm=1500,
        ),
        Transmission(forward_gears=[2.76, 1.7, 1.24, 1, 0.77], final_drive=2.88),
        Wheel(diameter_inches=26.2),
        weight_lbs=2400,
    )
