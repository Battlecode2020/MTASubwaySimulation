from dijkstar import Graph, find_path
import pandas as pd
import stations

def find_stations(all_stations, stop, line):
    for i in range(len(all_stations)):
        if all_stations[i].name == stop and all_stations[i].line == line:
            return all_stations[i]
    return None

def find_stations_exact(all_stations, line, complex):
    for i in range(len(all_stations)):
        if all_stations[i].line == line and all_stations[i].complex_id == complex:
            return all_stations[i]
    print("FAIL")
    return None


def add_line(graph, stops, train_frequency, station_transit, all_stations ):
    '''

    :param graph: Graph of train movement
    :param stops: the stops on the route in order
    :param train_frequency: the frequency at which trains go to each station. EX: every 15 minutes
    :param station_transit: time to get from one stop to the next. An array station_transit[0] = time from stops[0] to stops[1]
    :return:
    '''
    for i in range(len(station_transit)):
        graph.add_edge(stops[i], stops[i+1], (station_transit[i], stops[i].name + "-" + stops[i+1].name))
        graph.add_edge(stops[i+1], stops[i], (station_transit[i], stops[i+1].name + "-" + stops[i].name))
    for i in range(len(stops)):
        graph.add_edge(stops[i], find_stations_exact(all_stations, "O", stops[i].complex_id), (0, "Transfer from " + stops[i].line + " line"))
        graph.add_edge(find_stations_exact(all_stations, "O", stops[i].complex_id), stops[i], (train_frequency, "Transfer to " + stops[i].line + " line"))


def original_wait(station, line, time):
    print("HI")
def create_stations(filename):
    df = pd.read_csv(filename)
    all_stations = []
    complex_IDs = []
    for index,row in df.iterrows():
        lines = row['Daytime Routes'].split()
        for line in lines:
            all_stations.append(stations.Station(row['Stop Name'], line, row['Complex ID']))
        if row['Complex ID'] not in complex_IDs:
            all_stations.append(stations.Station(row['Stop Name'], "O", row['Complex ID']))
            complex_IDs.append(row['Complex ID'])
    return all_stations



def cost_func(u, v, edge, prev_edge):
    length, name = edge
    return length


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    subwayStations = create_stations("Subway_stations.csv")
    graph = Graph()
    # 1 line
    one_stop_names = ["South Ferry", "Rector St", "WTC Cortlandt", "Chambers St", "Franklin St", "Canal St", "Houston St", "Christopher St-Sheridan Sq", "14 St", "18 St", "23 St", "28 St", "34 St-Penn Station", "Times Sq-42 St", "50 St", "59 St-Columbus Circle", "66 St-Lincoln Center", "72 St", "79 St", "86 St", "96 St", "103 St", "Cathedral Pkwy (110 St)", "116 St-Columbia University", "125 St", "137 St-City College", "145 St", "157 St", "168 St-Washington Hts", "181 St", "191 St", "Dyckman St", "207 St", "215 St", "Marble Hill-225 St", "231 St", "238 St", "Van Cortlandt Park-242 St"]
    one_stops = []
    for i in one_stop_names:
        one_stops.append(find_stations(subwayStations, i, "1"))
    #South Ferry to Rector St first
    one_times = [2,1,1,1,1,2,2,2,1,1,1,1,1,2,2,2,1,1,1,2,1,2,1,2,2,1,2,2,3,1,1,1,1,3,1,1,5]
    add_line(graph, one_stops, 20, one_times, subwayStations)

    # 2 line
    two_stop_names = ["Flatbush Av-Brooklyn College", "Newkirk Av-Little Haiti", "Beverly Rd", "Church Av", "Winthrop St","Sterling St", "President St-Medgar Evers College", "Franklin Av-Medgar Evers College", "Eastern Pkwy-Brooklyn Museum", "Grand Army Plaza", "Bergen St", "Atlantic Av-Barclays Ctr", "Nevins St", "Hoyt St", "Borough Hall", "Clark St", "Wall St", "Fulton St", "Park Place", "Chambers St", "14 St", "34 St-Penn Station", "Times Sq-42 St", "72 St", "96 St", "Central Park North (110 St)", "116 St", "125 St", "135 St", "149 St-Grand Concourse", "3 Av-149 St", "Jackson Av", "Prospect Av", "Intervale Av", "Simpson St", "Freeman St", "174 St", "West Farms Sq-E Tremont Av", "E 180 St", "Bronx Park East", "Pelham Pkwy", "Allerton Av", "Burke Av", "Gun Hill Rd", "219 St", "225 St", "233 St","Nereid Av", "Wakefield-241 St"]
    two_stops = []
    for i in two_stop_names:
        two_stops.append(find_stations(subwayStations, i, "2"))
    two_times = [3,2,2,2,2,2,2,2,2,1,2,1,1,1,1,6,1,2,1,5,3,1,3,3,6,1,1,1,4,1,3,1,1,2,1,2,2,2,2,2,2,2,2,2,2,1,1,1]
    add_line(graph, two_stops, 8, two_times, subwayStations)


    # 3 line
    three_stop_names = ["Harlem-148 St", "145 St", "135 St", "125 St", "116 St", "Central Park North (110 St)", "96 St", "72 St", "Times Sq-42 St", "34 St-Penn Station", "14 St", "Chambers St", "Park Place", "Fulton St", "Wall St", "Clark St", "Borough Hall", "Hoyt St", "Nevins St", "Atlantic Av-Barclays Ctr", "Bergen St", "Grand Army Plaza","Eastern Pkwy-Brooklyn Museum", "Franklin Av-Medgar Evers College", "Nostrand Av", "Kingston Av", "Crown Hts-Utica Av", "Sutter Av-Rutland Rd", "Saratoga Av", "Rockaway Av", "Junius St", "Pennsylvania Av", "Van Siclen Av", "New Lots Av"]
    three_stops = []
    for i in three_stop_names:
        three_stops.append(find_stations(subwayStations, i, "3"))
    three_times = [1,2,1,1,1,6,3,4,1,3,4,1,2,1,6,1,1,1,1,2,1,2,1,1,2,2,2,2,2,2,2,1,1]
    add_line(graph, three_stops, 8, three_times, subwayStations)

    # 4 line
    four_stop_names = ["Woodlawn", "Mosholu Pkwy", "Bedford Park Blvd-Lehman College", "Kingsbridge Rd", "Fordham Rd", "183 St", "Burnside Av", "176 St", "Mt Eden Av", "170 St", "167 St", "161 St-Yankee Stadium", "149 St-Grand Concourse", "138 St-Grand Concourse", "125 St", "86 St", "59 St", "Grand Central-42 St", "14 St-Union Sq", "Brooklyn Bridge-City Hall", "Fulton St", "Wall St", "Bowling Green", "Borough Hall", "Nevins St", "Atlantic Av-Barclays Ctr", "Franklin Av-Medgar Evers College", "Crown Hts-Utica Av"]
    four_stops = []
    for i in four_stop_names:
        four_stops.append(find_stations(subwayStations, i, "4"))
    four_times = [1,2,2,2,1,1,1,1,1,2,3,2,2,2,5,4,2,3,5,2,1,1,7,2,1,4,3]
    add_line(graph, four_stops, 8, four_times, subwayStations)

    # 5 line
    five_stop_names = ["Eastchester-Dyre Av", "Baychester Av", "Gun Hill Rd", "Pelham Pkwy", "Morris Park", "E 180 St", "West Farms Sq-E Tremont Av", "174 St", "Freeman St", "Simpson St", "Intervale Av", "Prospect Av", "Jackson Av", "3 Av-149 St", "149 St-Grand Concourse", "138 St-Grand Concourse", "125 St", "86 St", "59 St", "Grand Central-42 St", "14 St-Union Sq", "Brooklyn Bridge-City Hall", "Fulton St", "Wall St", "Bowling Green", "Borough Hall", "Nevins St", "Atlantic Av-Barclays Ctr", "Franklin Av-Medgar Evers College", "President St-Medgar Evers College", "Sterling St", "Winthrop St", "Church Av", "Beverly Rd", "Newkirk Av-Little Haiti", "Flatbush Av-Brooklyn College"]
    five_stops = []
    for i in five_stop_names:
        five_stops.append(find_stations(subwayStations, i, "5"))
    five_times = [1,3,2,2,3,2,1,2,1,2,1,2,3,1,3,2,5,3,2,3,6,2,1,2,5,2,1,5,2,2,2,2,1,1,3]
    add_line(graph, five_stops, 8, five_times, subwayStations)

    # 6 line
    six_stop_names = ["Pelham Bay Park", "Buhre Av", "Middletown Rd", "Westchester Sq-E Tremont Av", "Zerega Av", "Castle Hill Av", "Parkchester", "St Lawrence Av", "Morrison Av-Soundview", "Elder Av", "Whitlock Av", "Hunts Point Av", "Longwood Av", "E 149 St", "E 143 St-St Mary's St", "Cypress Av", "Brook Av", "3 Av-138 St", "125 St", "116 St", "110 St", "103 St", "96 St", "86 St", "77 St","68 St-Hunter College","59 St", "51 St", "Grand Central-42 St", "33 St", "28 St", "23 St", "14 St-Union Sq", "Astor Pl", "Bleecker St", "Spring St", "Canal St", "Brooklyn Bridge-City Hall"]
    six_stops = []
    for i in six_stop_names:
        six_stops.append(find_stations(subwayStations, i, "6"))
    six_times = [2,2,2,2,1,1,1,2,1,1,2,1,1,1,2,2,2,3,1,1,2,2,2,2,1,2,1,2,2,1,1,1,1,3,1,1,2]
    add_line(graph, six_stops, 8, six_times, subwayStations)

    # 7 line

    # A line

    # B line

    # C line

    # D line

    # E line

    # Q line DAY ROUTE
    Q_stop_names = ["Coney Island-Stillwell Av", "W 8 St-NY Aquarium", "Ocean Pkwy", "Brighton Beach", "Sheepshead Bay", "Neck Rd", "Avenue U", "Kings Hwy", "Avenue M", "Avenue J", "Avenue H", "Newkirk Plaza", "Cortelyou Rd", "Beverley Rd", "Church Av", "Parkside Av", "Prospect Park", "7 Av", "Atlantic Av-Barclays Ctr", "DeKalb Av", "Canal St", "14 St-Union Sq", "34 St-Herald Sq", "Times Sq-42 St", "57 St-7 Av", "Lexington Av/63 St", "72 St", "86 St", "96 St"]
    Q_stops = []
    for i in Q_stop_names:
        Q_stops.append(find_stations(subwayStations, i, "Q"))
    Q_times = [2,2,1,1,1,2,3,2,2,2,1,1,1,1,2,2,3,3,2,8,4,3,2,2,3,2,2,2]
    add_line(graph, Q_stops, 8, Q_times, subwayStations)

    # R line
    R_stop_names = ["Bay Ridge-95 St", "86 St", "77 St", "Bay Ridge Av", "59 St", "53 St", "45 St", "36 St", "25 St", "Prospect Av", "4 Av-9 St", "Union St", "Atlantic Av-Barclays Ctr", "DeKalb Av", "Jay St-MetroTech", "Court St", "Whitehall St-South Ferry", "Rector St", "Cortlandt St", "City Hall", "Canal St", "Prince St", "8 St-NYU", "14 St-Union Sq", "23 St", "28 St","34 St-Herald Sq","Times Sq-42 St", "49 St", "57 St-7 Av", "5 Av/59 St", "Lexington Av/59 St", "Queens Plaza", "36 St", "Steinway St", "46 St", "Northern Blvd", "65 St", "Jackson Hts-Roosevelt Av", "Elmhurst Av", "Grand Av-Newtown", "Woodhaven Blvd", "63 Dr-Rego Park", "67 Av", "Forest Hills-71 Av"]
    R_stops = []
    for i in R_stop_names:
        R_stops.append(find_stations(subwayStations, i, "R"))
    R_times = [2,2,2,2,1,2,2,3,2,2,1,2,3,8,3,1,3,1,2,3,1,1,1,1,2,2,2,3,7,2,2,1,2,2,2,3,3,3,3]
    add_line(graph, R_stops, 7, R_times, subwayStations)


    print(find_path(graph, find_stations_exact(subwayStations, "O", 421), find_stations_exact(subwayStations, "O", 439), cost_func = cost_func))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
