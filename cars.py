from vehicle import Vehicle
from engine import Engine


def build_roku() -> Vehicle:

    return Vehicle()


def build_rally() -> Vehicle:

    return Vehicle(
        Engine(
            [
                (1000, 80),  # 1000 rpm, 80 ft-lb
                (2000, 120),  # 2000 rpm, 120 ft-lb
                (3000, 118),  # 3000 rpm, 150 ft-lb  turbo lag
                (3800, 150),  # 3800 rpm, 150 ft-lb spool begins
                (4100, 350),  # 4100 rpm, 350 ft-lb full boost
                (6600, 330),  # 6600 rpm, 330 ft-lb turbo fade
                (6800, 200),  # 6800 rpm, 200 ft-lb, turbo fade
                (6950, 11),
                (7000, 0),  # 7000 rpm fuel cutoff
            ]
        )
    )
