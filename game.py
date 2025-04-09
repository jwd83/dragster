from vehicle import Vehicle
import cars
from transmission import Transmission


def print_readout(vehicles: dict[Vehicle]):
    entries = []
    for name, v in vehicles.items():
        entries.append(f"{name},{v.readout()}")

    print(",".join(entries))


def main():

    vehicles = {
        "rally": cars.build_rally(),
        "roku": cars.build_econobox(),
    }

    while True:
        for _, v in vehicles.items():
            v.update()
            v.current_throttle = 1.0  # Full throttle

        if vehicles["rally"].ticks % 20 == 0:
            print_readout(vehicles)

        # check if any engine needs to be shifted up (shift at engine rpm above 6800)
        for _, v in vehicles.items():
            if v.current_engine_rpm > 6800:
                v.current_gear += 1

                # dont try to shift out of the max gear
                v.current_gear = min(v.transmission.max_gear, v.current_gear)

        # check if all vehicles have done a quarter mile
        all_done = True

        for _, v in vehicles.items():
            if v.odometer_miles < 0.25:
                all_done = False

        if all_done:
            break

    print_readout(vehicles)
    print("All vehicles have completed the quarter mile.")


if __name__ == "__main__":
    main()
