import datetime

TIME = datetime.datetime

STATIONS = []
ROUTES = []


def read_from_file(filename):
    global ROUTES, STATIONS
    file = open(filename)
    data = file.read()
    data = data.split("\n\n")
    for r in data:
        r = r.split("\n")
        name = r[1]
        stations = r[2]
        stations = stations.split(" ")
        STATIONS += stations
        intervals = r[3]
        intervals = intervals.split(" ")
        first = r[4]
        if first[0] == "0":
            first = first[1:]
        first = first.split(":")
        last = r[5]
        if last[0] == "0":
            last = last[1:]
        last = last.split(":")
        first_time = datetime.time(int(first[0]), int(first[1]))
        last_time = datetime.time(int(last[0]), int(last[1]))
        dict_stations = {}
        for i in range(len(stations)):
            dict_stations[stations[i]] = int(intervals[i])
        new_route = Route(r[0], len(stations), dict_stations, int(r[6]), first_time, last_time, name)
        ROUTES += [new_route]
    file.close()


def current_time():
    return TIME.now().time()


class Route:

    def __init__(self, vehicle, number_of_stations, stations, interval, first, last, name):
        self.name = name
        self.vehicle = vehicle
        self.number_of_stations = number_of_stations
        self.stations = stations
        self.interval = interval
        self.first = first.hour * 60 + first.minute
        if last.hour * 60 + last.minute < self.first:
            self.last = (last.hour + 24) * 60 + last.minute
        else:
            self.last = last.hour * 60 + last.minute

    def check_station(self, station):
        return station in self.stations.keys()

    def calculate_time_from_start(self, station):
        time = 0
        for stat in self.stations.keys():
            if station == stat:
                break
            time += self.stations[stat]
        return time

    def calculate_time_from_end(self, station):
        time = 0
        for stat in reversed(self.stations.keys()):
            time += self.stations[stat]
            if station == stat:
                break
        return time

    def next_department(self, station):
        time1 = self.calculate_time_from_start(station)
        time2 = self.calculate_time_from_end(station)
        curr_time = current_time().hour * 60 + current_time().minute
        if curr_time + 10 < self.first:
            curr_time += 24 * 60
        start_time = self.first
        while curr_time > start_time + time1 and start_time < self.last:
            start_time += self.interval
        first_time = start_time + time1 - curr_time

        start_time = self.first
        while curr_time > start_time + time2 and start_time < self.last:
            start_time += self.interval
        second_time = start_time + time2 - curr_time
        first_station = list(self.stations.keys())[0]
        last_station = list(self.stations.keys())[-1]
        if station == first_station:
            destinations = [(self.name, last_station, first_time)]
        elif station == last_station:
            destinations = [(self.name, first_station, second_time)]
        else:
            destinations = [(self.name, last_station, first_time),
                            (self.name, first_station, second_time)]
        return destinations

    def process_station(self, station):
        if self.check_station(station):
            return self.next_department(station)
        else:
            return []


read_from_file("departments_1.txt")
finished = False
while not finished:
    TIMETABLE = []

    print("Enter station: ")
    curr_station = input()
    if curr_station == "" or curr_station == "\n":
        break
    if curr_station in STATIONS:
        for route in ROUTES:
            TIMETABLE += route.process_station(curr_station)

        TIMETABLE = sorted(TIMETABLE, key=lambda department: department[2])

        if len(str(current_time().minute)) == 1:
            print("Current time: " + str(current_time().hour) + ":0" + str(current_time().minute))
        else:
            print("Current time: " + str(current_time().hour) + ":" + str(current_time().minute))
        empty = True
        for c in TIMETABLE:
            if 0 <= c[2] <= 10:
                print("Route: " + str(c[0]) + "  Destination: " + str(c[1]) + "  " + str(c[2]) + " min")
                empty = False
        if empty:
            print("No trains!")
    else:
        print("No such station!")
    print("")
