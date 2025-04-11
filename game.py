from vehicle import Vehicle
import cars
from transmission import Transmission
import datetime
import os
from csv import DictWriter


def print_readout(vehicles: dict[Vehicle]):
    entries = []
    for name, v in vehicles.items():
        entries.append(f"{name},{v.readout()}")

    print(",".join(entries))


def main():

    vehicles = {
        "rally": cars.build_rally(),
        "econobox": cars.build_econobox(),
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

    # make a timestamped folder inside ./logs
    folder_name = f"logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.makedirs(folder_name, exist_ok=True)
    print("Saving logs to:", folder_name)
    for name, v in vehicles.items():
        # save the readout to a file
        print(f"Saving {name} log of length {len(v.log)} to {folder_name}/{name}.csv")
        with open(f"{folder_name}/{name}.csv", "w") as f:
            data_log = v.log

            # get the field names from the first record
            fieldnames = data_log[0].keys()

            # create a csv writer object
            writer = DictWriter(f, fieldnames=fieldnames, lineterminator="\n")

            writer.writeheader()

            # write the data to the csv file
            for record in data_log:
                writer.writerow(record)

    # generate a merged log of all vehicles prefixing their columns with the vehicle name
    merged_log = []
    for i in range(len(vehicles["rally"].log)):
        merged_record = {}
        for name, v in vehicles.items():
            record = v.log[i]
            for key, value in record.items():
                merged_record[f"{name}_{key}"] = value
        merged_log.append(merged_record)

    # save the merged log to a file
    with open(f"{folder_name}/merged.csv", "w") as f:
        # get the field names from the first record
        fieldnames = merged_log[0].keys()

        # create a csv writer object
        writer = DictWriter(f, fieldnames=fieldnames, lineterminator="\n")

        writer.writeheader()

        # write the data to the csv file
        for record in merged_log:
            writer.writerow(record)


if __name__ == "__main__":
    main()
