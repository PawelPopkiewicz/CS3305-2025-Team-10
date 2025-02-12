def generate_trips():
    agency_id = None
    with open("back-end/static_gtfsr/agency.txt", "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
        for line in lines:
            line = line.split(",")
            if "Bus Éireann" == line[1]:
                agency_id = line[0]
                break
    route_ids = []
    with open('back-end/static_gtfsr/routes.txt', 'r', encoding="utf-8") as f:
        lines = f.read().splitlines()
        for line in lines:
            line = line.split(",")
            if line[1] == agency_id:
                if line[2] in ["201", "202", "203", "205", "206", "207", "208", "209", "212", "213",
                               "214", "215", "216", "219", "220", "223", "225", "226", "209A", "215A",
                               "207A", "226X", "202A", "225L", "220X", "223X"]:    # cork only
                    route_ids.append(line[0])

    with open('back-end/static_gtfsr/trips.txt', 'r', encoding="utf-8") as f:
        lines = f.read().splitlines()

    with open('back-end/static_gtfsr/cork_trip_ids.txt', 'w', encoding="utf-8") as f:
        header = lines[0]
        f.write(header + '\n')
        for line in lines[1:]:
            split_line = line.split(",")
            if split_line[0] in route_ids:
                f.write(split_line[2] + '\n')
    print("End")


def generate_stop_times():
    with open('back-end/static_gtfsr/cork_trip_ids.txt', 'r', encoding="utf-8") as f:
        trip_ids = set(f.read().splitlines())
    print("Opened trip ids")

    with open('back-end/static_gtfsr/stop_times.txt', 'r', encoding="utf-8") as f:
        lines = f.read().splitlines()
    print("Opened stop times")

    with open('back-end/static_gtfsr/cork_stop_times.txt', 'w', encoding="utf-8") as f:
        line_zero = lines[0]
        f.write(line_zero + '\n')
        for line in lines[1:]:
            split_line = line.split(",")
            if split_line[0] in trip_ids:
                f.write(line + '\n')
    print("End")


generate_trips()
generate_stop_times()
