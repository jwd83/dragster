"""

Cars are named after birds of colors that they resemble.

econobox - puffin (black and white)
rally car - blue jay (blue)
super car - cardinal (red) 475hp 2400lb
hyper car - green (1250hp 2200lb .35 drag 8 gears)
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
        drivetrain_efficiency=0.82,
    )


def budgie() -> Vehicle:

    budgie_engine = Engine(
        torque_curve=[
            (1000, 300),
            (2000, 400),
            (10500, 500),
            (11100, 400),
            (11101, 0),
        ],
        shift_rpm=10500,
        launch_rpm=1400,
    )  # fuel cut at >= 11,101 RPM

    budgie_transmission = Transmission(
        forward_gears=[3.6, 2.1, 1.4, 1.2, 1, 0.91, 0.85, 0.8],
        reverse_gear=4,
        final_drive=4,
    )

    budgie_wheel = Wheel((325, 30, 21))

    return Vehicle(
        budgie_engine,
        budgie_transmission,
        budgie_wheel,
        weight_lbs=2990,
        drag_coefficient=0.17,
        drivetrain_efficiency=0.89,
    )


def painted_bunting() -> Vehicle:

    return Vehicle(
        Engine(
            [(1000, 3000), (5000, 7400), (5500, 0)], shift_rpm=5000, launch_rpm=1000
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
        Wheel(tire_spec=(335, 35, 17)),
        weight_lbs=2400,
        drag_coefficient=0.34,
        drivetrain_efficiency=0.88,
    )
