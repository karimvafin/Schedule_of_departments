import datetime

TIME = datetime.datetime
ROUTES = []
STATIONS = []


def get_info(file_name):
    global ROUTES, STATIONS
    file = open(file_name)
    info = file.read()
    info = info.split("\n")
    for line in info:
        line = line.split("; ")
        stat = line[1].split(", ")
        STATIONS += stat
        intervals = line[2].split(", ") + ["0"]
        start_time = line[3]
        if start_time[0] == "0":
            start_time = start_time[1:]
        start_time = start_time.split(":")
        end_time = line[4]
        if end_time[0] == "0":
            end_time = end_time[1:]
        end_time = end_time.split(":")
        start = int(start_time[0]) * 60 + int(start_time[1])
        end = int(end_time[0]) * 60 + int(end_time[1])
        if end < start:
            end += 24 * 60
        stations = {}
        for i in range(len(stat)):
            stations[stat[i]] = int(intervals[i])
        new_route = (line[0], stations, start, end, int(line[5]))
        ROUTES += [new_route]
    file.close()


get_info("departments_2.txt")


def departments(station, route):
    if station in route[1].keys():
        time_from_start = 0
        time_from_end = 0
        for st in route[1].keys():
            if station == st:
                break
            time_from_start += route[1][st]
        for st in reversed(route[1].keys()):
            time_from_end += route[1][st]
            if station == st:
                break
        curr_time = TIME.now().time().hour * 60 + TIME.now().time().minute
        if curr_time + 10 < route[2]:
            curr_time += 24 * 60
        time_of_department_1 = route[2] + time_from_start
        time_of_department_2 = route[2] + time_from_end
        while curr_time > time_of_department_1 and time_of_department_1 < route[3]:
            time_of_department_1 += route[4]
        while curr_time > time_of_department_2 and time_of_department_2 < route[3]:
            time_of_department_2 += route[4]
        dt1 = time_of_department_1 - curr_time
        dt2 = time_of_department_2 - curr_time
        if station == list(route[1])[0]:
            deps = [(route[0], list(route[1])[-1], dt1)]
        elif station == list(route[1])[-1]:
            deps = [(route[0], list(route[1])[0], dt2)]
        else:
            deps = [(route[0], list(route[1])[-1], dt1), (route[0], list(route[1])[0], dt2)]
        return deps
    else:
        return []


while True:
    print("Enter station: ")
    current_station = input()
    DEPARTMENTS = []
    if current_station == "":
        break
    if current_station in STATIONS:
        for route in ROUTES:
            DEPARTMENTS += departments(current_station, route)

        DEPARTMENTS = sorted(DEPARTMENTS, key=lambda department: department[2])

        if len(str(TIME.now().time().minute)) == 1:
            print("Current time: " + str(TIME.now().time().hour) + ":0" + str(TIME.now().time().minute))
        else:
            print("Current time: " + str(TIME.now().time().hour) + ":" + str(TIME.now().time().minute))
        print("Schedule:")
        for dep in DEPARTMENTS:
            if 0 <= dep[2] <= 10:
                print(str(dep[0]) + ", destination " + str(dep[1]) + ", " + str(dep[2]) + " min")
    else:
        print("No such station!")
    print("")
