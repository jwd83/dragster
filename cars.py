from vehicle import Vehicle
from engine import Engine
from transmission import Transmission
from wheel import Wheel


def build_econobox() -> Vehicle:

    return Vehicle()


def build_rally() -> Vehicle:

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
        )
    )


def build_class_a() -> Vehicle:

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
    )
