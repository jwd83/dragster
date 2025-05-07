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


def print_race_results(title: str, results):

    print("\n" + "*" * 80 + f"\n{title}:" + "\n" + "-" * 80)
    for name, record in results.items():
        f_timing = f"{record['Time']:.3f}"
        f_timing = f"{f_timing:>8}"

        f_speed = f"{record['Speed']:.1f}"
        f_speed = f"{f_speed:>6}"

        print(f"{name:<20} -  {f_timing} sec  @ {f_speed} mph")


def main():

    vehicles = {
        "puffin": cars.puffin(),
        "blue_jay": cars.blue_jay(),
        "cardinal": cars.cardinal(),
        "budgie": cars.budgie(),
        "painted_bunting": cars.painted_bunting(),
    }

    while True:
        for _, v in vehicles.items():
            v.update()
            v.current_throttle = 1.0  # Full throttle

        # if vehicles["blue_jay"].ticks % 20 == 0:
        #     print_readout(vehicles)

        # check if any engine needs to be shifted up
        for _, v in vehicles.items():
            if v.current_engine_rpm > v.engine.shift_rpm:
                v.current_gear += 1

                # dont try to shift out of the max gear
                v.current_gear = min(v.transmission.max_gear, v.current_gear)

        # check if all vehicles have done a quarter mile
        all_done = True

        for _, v in vehicles.items():
            if v.odometer_miles < 5:
                all_done = False

        if all_done:
            break

    # print_readout(vehicles)
    print("All vehicles have completed the race.")

    quarter_mile_results = {}
    standing_mile_results = {}
    five_mile_results = {}

    for name, v in vehicles.items():
        for record in v.log:
            if record["Distance"] >= 5:
                five_mile_results[name] = record
                break

        for record in v.log:
            if record["Distance"] >= 1:
                standing_mile_results[name] = record
                break

        for record in v.log:
            if record["Distance"] >= 0.25:
                quarter_mile_results[name] = record
                break

    print_race_results("QUARTER MILE", quarter_mile_results)
    print_race_results("STANDING MILE", standing_mile_results)
    print_race_results("FIVE MILE", five_mile_results)

    print("*" * 80)

    # make a timestamped folder inside ./logs
    folder_name = f"logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
    os.makedirs(folder_name, exist_ok=True)
    print("Saving logs to:", folder_name)
    for name, v in vehicles.items():
        # save the readout to a file
        # print(f"Saving {name} log of length {len(v.log)} to {folder_name}/{name}.csv")
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
    for i in range(len(vehicles["blue_jay"].log)):
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
