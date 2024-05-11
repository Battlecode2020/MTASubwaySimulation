from dijkstar import Graph, find_path
import pandas as pd
import stations
import simulation
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import Isomap
def find_stations(all_stations, stop, line):
    for i in range(len(all_stations)):
        if all_stations[i].name == stop and all_stations[i].line == line:
            return all_stations[i]
    return None

def find_stations_exact(all_stations, line, complex):
    for i in range(len(all_stations)):
        if all_stations[i].line == line and all_stations[i].complex_id == complex:
            return all_stations[i]
    print("FAIL {} {}".format(line, complex))
    return None

def find_stations_of_complex(all_stations, complex):
    complex_stations = []
    for i in range(len(all_stations)):
        if all_stations[i].complex_id == complex:
            complex_stations.append(all_stations[i])
    return complex_stations



def add_line(graph, stops, train_frequency, station_transit, all_stations ):
    '''

    :param graph: Graph of train movement
    :param stops: the stops on the route in order
    :param train_frequency: the frequency at which trains go to each station. EX: every 15 minutes
    :param station_transit: time to get from one stop to the next. An array station_transit[0] = time from stops[0] to stops[1]
    :return:
    '''
    if len(stops) - len(station_transit) != 1:
        raise Exception
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

def get_complexes(filename="Subway_stations.csv"):
    banned = [627,141,626,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,444,445,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,522,523]
    #think about gun hill rd and pelham pkwy

    df = pd.read_csv(filename)
    complex_IDs = []
    for index, row in df.iterrows():
        lines = row['Daytime Routes'].split()

        if (row['Complex ID'] not in banned) and (row['Complex ID'] not in complex_IDs):
            complex_IDs.append(row['Complex ID'])
    return complex_IDs

def get_graph():
    '''
    # 1 PM
    line_freqs = {'1': 6, '2': 8, '3': 8, '4': 8, '5': 8, '6': 4, '7': 5, 'A': 8, 'B': 10, 'C': 8, 'D': 10, 'E': 8, 'F': 7, 'G': 8, 'J': 10, 'L': 5, 'M': 10, 'N': 9, 'Q': 9, 'S': 5, 'R': 8, 'W': 10}

    #4 PM
    line_freqs = {'1': 5, '2': 6, '3': 7, '4': 6, '5': 4, '6': 4, '7': 3, 'A': 6, 'B': 10, 'C': 10, 'D': 6, 'E': 5, 'F': 5, 'G': 8, 'J': 9, 'L': 4, 'M': 7, 'N': 12, 'Q': 8, 'S': 5, 'R': 7, 'W': 10}

    #7 PM
    line_freqs = {'1': 4, '2': 6, '3': 7, '4': 6, '5': 9, '6': 4, '7': 3, 'A': 8, 'B': 10, 'C': 7, 'D': 10, 'E': 5, 'F': 5, 'G': 9, 'J': 10, 'L': 4, 'M': 11, 'N': 10, 'Q': 7, 'S': 5, 'R': 11, 'W': 10}

    #10 PM
    line_freqs = {'1': 5, '2': 10, '3': 15, '4': 10, '5': 18, '6': 7, '7': 5, 'A': 10, 'B': 60, 'C': 11, 'D': 12, 'E': 10, 'F': 10, 'G': 12, 'J': 10, 'L': 6, 'M': 10, 'N': 10, 'Q': 10, 'S': 5, 'R': 12, 'W': 10}
    '''
    #2 AM
    line_freqs = {'1': 20, '2': 20, '3': 20, '4': 20, '5': 20, '6': 20, '7': 20, 'A': 20, 'B': 60, 'C': 60, 'D': 20, 'E': 20,  'F': 20, 'G': 20, 'J': 20, 'L': 20, 'M': 20, 'N': 20, 'Q': 20, 'S': 60, 'R': 20, 'W': 60}
    '''
    #10 AM
    line_freqs = {'1': 5, '2': 8, '3': 8, '4': 7, '5': 8, '6': 4, '7': 5, 'A': 5, 'B': 10, 'C': 10, 'D': 10, 'E': 6, 'F': 6, 'G': 7, 'J': 10, 'L': 4, 'M': 10, 'N': 9, 'Q': 8, 'S': 4, 'R': 8, 'W': 10}
    #7 AM
    line_freqs = {'1': 8, '2': 6, '3': 6, '4': 5, '5': 4, '6': 4, '7': 2, 'A': 4, 'B': 6, 'C': 10, 'D': 10, 'E': 6, 'F': 4, 'G': 7, 'J': 10, 'L': 4, 'M': 9, 'N': 10, 'Q': 7, 'S': 5, 'R': 8, 'W': 9}
    '''
    subwayStations = create_stations("Subway_stations.csv")
    graph = Graph()
    # 1 line
    one_stop_names = ["South Ferry", "Rector St", "WTC Cortlandt", "Chambers St", "Franklin St", "Canal St", "Houston St", "Christopher St-Sheridan Sq", "14 St", "18 St", "23 St", "28 St", "34 St-Penn Station", "Times Sq-42 St", "50 St", "59 St-Columbus Circle", "66 St-Lincoln Center", "72 St", "79 St", "86 St", "96 St", "103 St", "Cathedral Pkwy (110 St)", "116 St-Columbia University", "125 St", "137 St-City College", "145 St", "157 St", "168 St-Washington Hts", "181 St", "191 St", "Dyckman St", "207 St", "215 St", "Marble Hill-225 St", "231 St", "238 St", "Van Cortlandt Park-242 St"]
    one_stops = []
    for i in one_stop_names:
        one_stops.append(find_stations(subwayStations, i, "1"))
    #South Ferry to Rector St first
    one_times = [2,1,1,1,1,2,2,2,1,1,1,1,1,2,2,2,1,1,1,2,1,2,1,2,2,1,2,2,3,1,1,1,1,3,1,1,5]
    add_line(graph, one_stops, line_freqs['1'], one_times, subwayStations)

    # 2 line
    two_stop_names = ["Flatbush Av-Brooklyn College", "Newkirk Av-Little Haiti", "Beverly Rd", "Church Av", "Winthrop St","Sterling St", "President St-Medgar Evers College", "Franklin Av-Medgar Evers College", "Eastern Pkwy-Brooklyn Museum", "Grand Army Plaza", "Bergen St", "Atlantic Av-Barclays Ctr", "Nevins St", "Hoyt St", "Borough Hall", "Clark St", "Wall St", "Fulton St", "Park Place", "Chambers St", "14 St", "34 St-Penn Station", "Times Sq-42 St", "72 St", "96 St", "Central Park North (110 St)", "116 St", "125 St", "135 St", "149 St-Grand Concourse", "3 Av-149 St", "Jackson Av", "Prospect Av", "Intervale Av", "Simpson St", "Freeman St", "174 St", "West Farms Sq-E Tremont Av", "E 180 St", "Bronx Park East", "Pelham Pkwy", "Allerton Av", "Burke Av", "Gun Hill Rd", "219 St", "225 St", "233 St","Nereid Av", "Wakefield-241 St"]
    two_stops = []
    for i in two_stop_names:
        two_stops.append(find_stations(subwayStations, i, "2"))
    two_times = [3,2,2,2,2,2,2,2,2,1,2,1,1,1,1,6,1,2,1,5,3,1,3,3,6,1,1,1,4,1,3,1,1,2,1,2,2,2,2,2,2,2,2,2,2,1,1,1]
    add_line(graph, two_stops, line_freqs['2'], two_times, subwayStations)


    # 3 line
    three_stop_names = ["Harlem-148 St", "145 St", "135 St", "125 St", "116 St", "Central Park North (110 St)", "96 St", "72 St", "Times Sq-42 St", "34 St-Penn Station", "14 St", "Chambers St", "Park Place", "Fulton St", "Wall St", "Clark St", "Borough Hall", "Hoyt St", "Nevins St", "Atlantic Av-Barclays Ctr", "Bergen St", "Grand Army Plaza","Eastern Pkwy-Brooklyn Museum", "Franklin Av-Medgar Evers College", "Nostrand Av", "Kingston Av", "Crown Hts-Utica Av", "Sutter Av-Rutland Rd", "Saratoga Av", "Rockaway Av", "Junius St", "Pennsylvania Av", "Van Siclen Av", "New Lots Av"]
    three_stops = []
    for i in three_stop_names:
        three_stops.append(find_stations(subwayStations, i, "3"))
    three_times = [1,2,1,1,1,6,3,4,1,3,4,1,2,1,6,1,1,1,1,2,1,2,1,1,2,2,2,2,2,2,2,1,1]
    add_line(graph, three_stops, line_freqs['3'], three_times, subwayStations)

    # 4 line
    four_stop_names = ["Woodlawn", "Mosholu Pkwy", "Bedford Park Blvd-Lehman College", "Kingsbridge Rd", "Fordham Rd", "183 St", "Burnside Av", "176 St", "Mt Eden Av", "170 St", "167 St", "161 St-Yankee Stadium", "149 St-Grand Concourse", "138 St-Grand Concourse", "125 St", "86 St", "59 St", "Grand Central-42 St", "14 St-Union Sq", "Brooklyn Bridge-City Hall", "Fulton St", "Wall St", "Bowling Green", "Borough Hall", "Nevins St", "Atlantic Av-Barclays Ctr", "Franklin Av-Medgar Evers College", "Crown Hts-Utica Av"]
    four_stops = []
    for i in four_stop_names:
        four_stops.append(find_stations(subwayStations, i, "4"))
    four_times = [1,2,2,2,1,1,1,1,1,2,3,2,2,2,5,4,2,3,5,2,1,1,7,2,1,4,3]
    add_line(graph, four_stops, line_freqs['4'], four_times, subwayStations)

    # 5 line
    five_stop_names = ["Eastchester-Dyre Av", "Baychester Av", "Gun Hill Rd", "Pelham Pkwy", "Morris Park", "E 180 St", "West Farms Sq-E Tremont Av", "174 St", "Freeman St", "Simpson St", "Intervale Av", "Prospect Av", "Jackson Av", "3 Av-149 St", "149 St-Grand Concourse", "138 St-Grand Concourse", "125 St", "86 St", "59 St", "Grand Central-42 St", "14 St-Union Sq", "Brooklyn Bridge-City Hall", "Fulton St", "Wall St", "Bowling Green", "Borough Hall", "Nevins St", "Atlantic Av-Barclays Ctr", "Franklin Av-Medgar Evers College", "President St-Medgar Evers College", "Sterling St", "Winthrop St", "Church Av", "Beverly Rd", "Newkirk Av-Little Haiti", "Flatbush Av-Brooklyn College"]
    five_stops = []
    for i in five_stop_names:
        five_stops.append(find_stations(subwayStations, i, "5"))
    five_times = [1,3,2,2,3,2,1,2,1,2,1,2,3,1,3,2,5,3,2,3,6,2,1,2,5,2,1,5,2,2,2,2,1,1,3]
    add_line(graph, five_stops, line_freqs['5'], five_times, subwayStations)

    # 6 line
    six_stop_names = ["Pelham Bay Park", "Buhre Av", "Middletown Rd", "Westchester Sq-E Tremont Av", "Zerega Av", "Castle Hill Av", "Parkchester", "St Lawrence Av", "Morrison Av-Soundview", "Elder Av", "Whitlock Av", "Hunts Point Av", "Longwood Av", "E 149 St", "E 143 St-St Mary's St", "Cypress Av", "Brook Av", "3 Av-138 St", "125 St", "116 St", "110 St", "103 St", "96 St", "86 St", "77 St","68 St-Hunter College","59 St", "51 St", "Grand Central-42 St", "33 St", "28 St", "23 St", "14 St-Union Sq", "Astor Pl", "Bleecker St", "Spring St", "Canal St", "Brooklyn Bridge-City Hall"]
    six_stops = []
    for i in six_stop_names:
        six_stops.append(find_stations(subwayStations, i, "6"))
    six_times = [2,2,2,2,1,1,1,2,1,1,2,1,1,1,2,2,2,3,1,1,2,2,2,2,1,2,1,2,2,1,1,1,1,3,1,1,2]
    add_line(graph, six_stops, line_freqs['6'], six_times, subwayStations)

    # 7 line
    seven_stop_names = ["34 St-Hudson Yards", "Times Sq-42 St", "5 Av", "Grand Central-42 St", "Vernon Blvd-Jackson Av", "Hunters Point Av", "Court Sq", "Queensboro Plaza", "33 St-Rawson St", "40 St-Lowery St", "46 St-Bliss St", "52 St", "61 St-Woodside", "69 St", "74 St-Broadway", "82 St-Jackson Hts", "90 St-Elmhurst Av", "Junction Blvd", "103 St-Corona Plaza", "111 St", "Mets-Willets Point", "Flushing-Main St"]
    seven_stops = []
    for i in seven_stop_names:
        seven_stops.append(find_stations(subwayStations, i, "7"))
    seven_times = [3,2,1,4,1,2,2,2,1,2,1,1,2,2,1,1,1,1,1,2,2]
    add_line(graph, seven_stops, line_freqs['7'], seven_times, subwayStations)

    # A line
    A_stop_names = ["Inwood-207 St", "Dyckman St", "190 St", "181 St", "175 St", "168 St", "145 St", "125 St", "59 St-Columbus Circle", "42 St-Port Authority Bus Terminal", "34 St-Penn Station", "14 St", "W 4 St-Wash Sq", "Canal St", "Chambers St", "Fulton St", "High St", "Jay St-MetroTech", "Hoyt-Schermerhorn Sts", "Nostrand Av", "Utica Av", "Broadway Junction", "Euclid Av", "Grant Av", "80 St", "88 St", "Rockaway Blvd"]
    A_stops = []
    for i in A_stop_names:
        A_stops.append(find_stations(subwayStations, i, "A"))
    A_times = [3,2,2,3,3,5,3,7,5,1,2,4,2,1,2,4,1,2,5,2,4,4,2,2,1,1 ]
    add_line(graph, A_stops, line_freqs['A'], A_times, subwayStations)

    # B line
    B_stop_names = ["Bedford Park Blvd", "Kingsbridge Rd", "Fordham Rd", "182-183 Sts", "Tremont Av", "174-175 Sts", "170 St", "167 St", "161 St-Yankee Stadium", "155 St", "145 St", "135 St", "125 St", "116 St", "Cathedral Pkwy (110 St)", "103 St", "96 St", "86 St", "81 St-Museum of Natural History", "72 St", "59 St-Columbus Circle", "7 Av", "47-50 Sts-Rockefeller Ctr", "42 St-Bryant Pk", "34 St-Herald Sq", "W 4 St-Wash Sq", "Broadway-Lafayette St", "Grand St", "DeKalb Av", "Atlantic Av-Barclays Ctr", "7 Av", "Prospect Park", "Church Av", "Newkirk Plaza", "Kings Hwy", "Sheepshead Bay", "Brighton Beach" ]
    B_stops = []
    for i in B_stop_names:
        B_stops.append(find_stations(subwayStations, i, "B"))
    B_times = [2,2,2,1,1,1,1,2,4,2,3,2,1,1,2,2,1,1,1,3,2,2,2,1,3,2,2,8,2,2,3,3,2,5,4,2]
    add_line(graph, B_stops, line_freqs['B'], B_times, subwayStations)

    # C line
    C_stop_names = ["168 St", "163 St-Amsterdam Av", "155 St", "145 St", "135 St", "125 St", "116 St", "Cathedral Pkwy (110 St)", "103 St", "96 St", "86 St", "81 St-Museum of Natural History", "72 St", "59 St-Columbus Circle", "50 St", "42 St-Port Authority Bus Terminal", "34 St-Penn Station", "23 St", "14 St", "W 4 St-Wash Sq", "Spring St", "Canal St", "Chambers St", "Fulton St", "High St", "Jay St-MetroTech", "Hoyt-Schermerhorn Sts", "Lafayette Av", "Clinton-Washington Avs", "Franklin Av", "Nostrand Av", "Kingston-Throop Avs", "Utica Av", "Ralph Av", "Rockaway Av", "Broadway Junction", "Liberty Av", "Van Siclen Av", "Shepherd Av", "Euclid Av"]
    C_stops = []
    for i in C_stop_names:
        C_stops.append(find_stations(subwayStations, i, "C"))
    C_times = [1,2,1,2,2,1,1,2,1,1,1,1,3,2,2,1,1,1,3,2,1,1,2,5,1,2,2,1,2,1,1,2,1,1,2,4,2,3,3]
    add_line(graph, C_stops, line_freqs['C'], C_times, subwayStations)

    # D line - TIMES WITH BROOKLYN LOCAL - CHECK
    D_stop_names = ["Norwood-205 St", "Bedford Park Blvd", "Kingsbridge Rd", "Fordham Rd", "182-183 Sts", "Tremont Av", "174-175 Sts", "170 St", "167 St", "161 St-Yankee Stadium", "155 St", "145 St", "125 St", "59 St-Columbus Circle", "7 Av", "47-50 Sts-Rockefeller Ctr", "42 St-Bryant Pk", "34 St-Herald Sq", "W 4 St-Wash Sq", "Broadway-Lafayette St", "Grand St", "Atlantic Av-Barclays Ctr", "36 St", "9 Av", "Fort Hamilton Pkwy", "50 St", "55 St", "62 St", "71 St", "79 St", "18 Av", "20 Av", "Bay Pkwy", "25 Av", "Bay 50 St", "Coney Island-Stillwell Av"]
    D_stops = []
    for i in D_stop_names:
        D_stops.append(find_stations(subwayStations, i, "D"))
    D_times = [2,2,2,2,2,1,1,1,2,4,2,3,8,2,2,1,1,3,2,2,13,9,3,2,3,2,3,2,2,2,2,2,3,4,4]
    add_line(graph, D_stops, line_freqs['D'], D_times, subwayStations)
    # E line
    E_stop_names = ["Jamaica Center-Parsons/Archer", "Sutphin Blvd-Archer Av-JFK Airport", "Jamaica-Van Wyck", "Briarwood", "Kew Gardens-Union Tpke", "75 Av", "Forest Hills-71 Av", "Jackson Hts-Roosevelt Av", "Queens Plaza", "Court Sq-23 St", "Lexington Av/53 St", "5 Av/53 St", "7 Av", "50 St", "42 St-Port Authority Bus Terminal", "34 St-Penn Station", "23 St", "14 St", "W 4 St-Wash Sq", "Spring St","Canal St", "World Trade Center" ]
    E_stops = []
    for i in E_stop_names:
        E_stops.append(find_stations(subwayStations, i, "E"))
    E_times = [1,2,2,2,1,1,7,6,1,4,1,2,3,2,1,1,1,3,2,1,1]
    add_line(graph, E_stops, line_freqs['E'], E_times, subwayStations)
    # F line
    F_stop_names = ["Jamaica-179 St", "169 St", "Parsons Blvd", "Sutphin Blvd", "Briarwood", "Kew Gardens-Union Tpke", "75 Av", "Forest Hills-71 Av", "Jackson Hts-Roosevelt Av", "21 St-Queensbridge", "Roosevelt Island", "Lexington Av/63 St", "57 St", "47-50 Sts-Rockefeller Ctr", "42 St-Bryant Pk", "34 St-Herald Sq", "23 St", "14 St", "W 4 St-Wash Sq", "Broadway-Lafayette St","2 Av", "Delancey St-Essex St", "East Broadway", "York St", "Jay St-MetroTech", "Bergen St", "Carroll St", "Smith-9 Sts", "4 Av-9 St", "7 Av", "15 St-Prospect Park", "Fort Hamilton Pkwy", "Church Av", "Ditmas Av", "18 Av", "Avenue I", "Bay Pkwy", "Avenue N", "Avenue P", "Kings Hwy", "Avenue U", "Avenue X", "Neptune Av", "W 8 St-NY Aquarium", "Coney Island-Stillwell Av"]
    F_stops = []
    for i in F_stop_names:
        F_stops.append(find_stations(subwayStations, i, "F"))
    F_times = [4,4,4,5,5,1,2,10,11,2,2,3,2,1,1,1,2,2,2,1,1,1,4,2,3,1,1,2,2,1,3,1,2,1,1,1,3,1,1,2,2,1,2,2]
    add_line(graph, F_stops, line_freqs['F'], F_times, subwayStations)


    # G LINE
    G_stop_names = ["Court Sq", "21 St", "Greenpoint Av", "Nassau Av", "Metropolitan Av", "Broadway", "Flushing Av", "Myrtle-Willoughby Avs", "Bedford-Nostrand Avs", "Classon Av", "Clinton-Washington Avs", "Fulton St", "Hoyt-Schermerhorn Sts", "Bergen St", "Carroll St", "Smith-9 Sts", "4 Av-9 St", "7 Av", "15 St-Prospect Park", "Fort Hamilton Pkwy", "Church Av"]
    G_stops = []
    for i in G_stop_names:
        G_stops.append(find_stations(subwayStations, i, "G"))
    G_times = [1,3,1,2,2,2,1,2,1,1,1,3,2,1,2,2,2,1,2,1]
    add_line(graph, G_stops, line_freqs['G'], G_times, subwayStations)

    #J LINE
    J_stop_names = ["Broad St", "Fulton St", "Chambers St", "Canal St", "Bowery", "Delancey St-Essex St", "Marcy Av", "Hewes St", "Lorimer St", "Flushing Av", "Myrtle Av", "Kosciuszko St", "Gates Av", "Halsey St", "Chauncey St", "Broadway Junction", "Alabama Av", "Van Siclen Av", "Cleveland St", "Norwood Av", "Crescent St", "Cypress Hills", "75 St-Elderts Ln", "85 St-Forest Pkwy", "Woodhaven Blvd", "104 St", "111 St", "121 St", "Sutphin Blvd-Archer Av-JFK Airport", "Jamaica Center-Parsons/Archer"]
    J_stops = []
    for i in J_stop_names:
        J_stops.append(find_stations(subwayStations, i, "J"))
    J_times = [2,1,1,2,2,8,1,2,1,2,1,2,1,1,2,2,2,1,1,1,2,1,2,2,3,2,1,4,1]
    add_line(graph, J_stops, line_freqs['J'], J_times, subwayStations)

    #L line
    L_stop_names = ["8 Av", "6 Av", "14 St-Union Sq", "3 Av", "1 Av", "Bedford Av", "Lorimer St", "Graham Av", "Grand St", "Montrose Av", "Morgan Av", "Jefferson St", "DeKalb Av", "Myrtle-Wyckoff Avs", "Halsey St", "Wilson Av", "Bushwick Av-Aberdeen St", "Broadway Junction", "Atlantic Av", "Sutter Av", "Livonia Av", "New Lots Av", "East 105 St", "Canarsie-Rockaway Pkwy"]
    L_stops = []
    for i in L_stop_names:
        L_stops.append(find_stations(subwayStations, i, "L"))
    L_times = [2,1,1,1,4,2,1,1,1,1,3,1,2,2,2,1,2,2,2,1,2,1,2]
    add_line(graph, L_stops, line_freqs['L'], L_times, subwayStations)

    #M LINE
    M_stop_names = ["Forest Hills-71 Av", "67 Av", "63 Dr-Rego Park", "Woodhaven Blvd", "Grand Av-Newtown", "Elmhurst Av", "Jackson Hts-Roosevelt Av", "65 St", "Northern Blvd", "46 St", "Steinway St", "36 St", "Queens Plaza", "Court Sq-23 St", "Lexington Av/53 St", "5 Av/53 St", "47-50 Sts-Rockefeller Ctr", "42 St-Bryant Pk", "34 St-Herald Sq", "23 St", "14 St", "W 4 St-Wash Sq", "Broadway-Lafayette St", "Delancey St-Essex St", "Marcy Av", "Hewes St", "Lorimer St", "Flushing Av", "Myrtle Av", "Central Av", "Knickerbocker Av", "Myrtle-Wyckoff Avs", "Seneca Av", "Forest Av", "Fresh Pond Rd", "Middle Village-Metropolitan Av"]
    M_stops = []
    for i in M_stop_names:
        M_stops.append(find_stations(subwayStations, i, "M"))
    M_times = [2,2,2,1,2,1,2,2,1,1,2,3,1,3,2,2,2,1,2,1,2,2,3,8,1,1,1,2,3,2,1,2,2,1,2]
    add_line(graph, M_stops, line_freqs['M'], M_times, subwayStations)

    #N LINE
    N_stop_names = ["Astoria-Ditmars Blvd", "Astoria Blvd", "30 Av", "Broadway", "36 Av", "39 Av-Dutch Kills", "Queensboro Plaza", "Lexington Av/59 St", "5 Av/59 St", "57 St-7 Av", "49 St", "Times Sq-42 St", "34 St-Herald Sq", "14 St-Union Sq", "Canal St", "Atlantic Av-Barclays Ctr", "36 St", "59 St", "8 Av", "Fort Hamilton Pkwy", "New Utrecht Av", "18 Av", "20 Av", "Bay Pkwy", "Kings Hwy", "Avenue U", "86 St", "Coney Island-Stillwell Av"]
    N_stops = []
    for i in N_stop_names:
        N_stops.append(find_stations(subwayStations, i, "N"))
    N_times = [2,2,2,1,2,1,5,1,3,2,2,2,3,5,12,8,4,2,2,2,3,1,1,1,3,1,4]
    add_line(graph, N_stops, line_freqs['N'], N_times, subwayStations)

    # Q line DAY ROUTE
    Q_stop_names = ["Coney Island-Stillwell Av", "W 8 St-NY Aquarium", "Ocean Pkwy", "Brighton Beach", "Sheepshead Bay", "Neck Rd", "Avenue U", "Kings Hwy", "Avenue M", "Avenue J", "Avenue H", "Newkirk Plaza", "Cortelyou Rd", "Beverley Rd", "Church Av", "Parkside Av", "Prospect Park", "7 Av", "Atlantic Av-Barclays Ctr", "DeKalb Av", "Canal St", "14 St-Union Sq", "34 St-Herald Sq", "Times Sq-42 St", "57 St-7 Av", "Lexington Av/63 St", "72 St", "86 St", "96 St"]
    Q_stops = []
    for i in Q_stop_names:
        Q_stops.append(find_stations(subwayStations, i, "Q"))
    Q_times = [2,2,1,1,1,2,3,2,2,2,1,1,1,1,2,2,3,3,2,8,4,3,2,2,3,2,2,2]
    add_line(graph, Q_stops, line_freqs['Q'], Q_times, subwayStations)

    #S line
    S_stop_names = ["Times Sq-42 St", "Grand Central-42 St"]
    S_stops = []
    for i in S_stop_names:
        S_stops.append(find_stations(subwayStations, i, "S"))
    S_times = [2]
    add_line(graph, S_stops, line_freqs['S'], S_times, subwayStations)

    # R line
    R_stop_names = ["Bay Ridge-95 St", "86 St", "77 St", "Bay Ridge Av", "59 St", "53 St", "45 St", "36 St", "25 St", "Prospect Av", "4 Av-9 St", "Union St", "Atlantic Av-Barclays Ctr", "DeKalb Av", "Jay St-MetroTech", "Court St", "Whitehall St-South Ferry", "Rector St", "Cortlandt St", "City Hall", "Canal St", "Prince St", "8 St-NYU", "14 St-Union Sq", "23 St", "28 St","34 St-Herald Sq","Times Sq-42 St", "49 St", "57 St-7 Av", "5 Av/59 St", "Lexington Av/59 St", "Queens Plaza", "36 St", "Steinway St", "46 St", "Northern Blvd", "65 St", "Jackson Hts-Roosevelt Av", "Elmhurst Av", "Grand Av-Newtown", "Woodhaven Blvd", "63 Dr-Rego Park", "67 Av", "Forest Hills-71 Av"]
    R_stops = []
    for i in R_stop_names:
        R_stops.append(find_stations(subwayStations, i, "R"))
    R_times = [1,2,1,3,2,2,2,2,2,2,1,2,3,1,1,5,2,1,2,2,1,2,1,2,1,1,2,1,2,2,1,6,2,2,1,2,2,2,1,2,1,2,2,2]
    add_line(graph, R_stops, line_freqs['R'], R_times, subwayStations)

    #W line
    W_stop_names = ["Astoria-Ditmars Blvd", "Astoria Blvd", "30 Av", "Broadway", "36 Av", "39 Av-Dutch Kills", "Queensboro Plaza", "Lexington Av/59 St", "5 Av/59 St", "57 St-7 Av", "49 St", "Times Sq-42 St", "34 St-Herald Sq", "28 St","23 St","14 St-Union Sq", "8 St-NYU", "Prince St", "Canal St", "City Hall", "Cortlandt St", "Rector St", "Whitehall St-South Ferry" ]
    W_stops = []
    for i in W_stop_names:
        W_stops.append(find_stations(subwayStations, i, "W"))
    W_times = [2, 2, 2, 1, 2, 1, 5, 1, 3, 2, 2, 2,1,1,2,1,3,2,2,2,1,2]
    add_line(graph, W_stops, line_freqs['W'], W_times, subwayStations)

    #Z line
    Z_stop_names = []

    return graph, subwayStations

def total_time(graph, all_stations, movement_matrix):
    banned = [627, 141, 626, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 444,445, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 522,523]
    total = 0
    for i in range(len(movement_matrix)):
        for j in range(len(movement_matrix[i])):
            if i not in banned and j not in banned and movement_matrix[i][j] != 0:
                total += movement_matrix[i][j] * find_path(graph, find_stations_exact(all_stations, "O", i), find_stations_exact(all_stations, "O", j), cost_func=cost_func).total_cost
    return total
if __name__ == '__main__':
    color = {}
    color['A'] = 'b'
    color['B'] = 'orange'
    color['C'] = 'b'
    color['D'] = 'orange'
    color['E'] = 'b'
    color['F'] = 'orange'
    color['G'] = 'g'
    color['J'] = 'brown'
    color['M'] = 'orange'
    color['N'] = 'yellow'
    color['Q'] = 'yellow'
    color['R'] = 'yellow'
    color['S'] = 'gray'
    color['W'] = 'yellow'
    color['Z'] = 'brown'
    color['O'] = 'k'
    color['1'] = 'r'
    color['6'] = 'g'
    color['2'] = 'r'
    color['3'] = 'r'
    color['4'] = 'g'
    color['5'] = 'g'
    color['7'] = 'purple'

    graph, substations = get_graph()
    current_time = "10/17/2023 05:00:00 AM"
    for i in range(4):
        print("{}: {}".format(current_time, total_time(graph, substations, simulation.movement(current_time))))
        current_time = simulation.nextTime(current_time)
    locs = get_complexes()
    included_stations = []
    '''
    for i in locs:
        included_stations.extend(find_stations_of_complex(substations,i))
    '''
    for i in locs:
        included_stations.append(find_stations_exact(substations, "O", i))
    distances = np.zeros((len(included_stations), len(included_stations)))
    for i in range(len(included_stations)):
        for j in range(len(included_stations)):
            distances[i][j] = find_path(graph, included_stations[i], included_stations[j], cost_func=cost_func).total_cost
            print("{} {}".format(i, j))

    isomap = Isomap(n_neighbors=10, n_components=2)
    X_iso = isomap.fit_transform(distances)
    # Plotting the result
    plt.figure(figsize=(8, 6))
    for i in range(len(included_stations)):
        plt.scatter(X_iso[i, 0], X_iso[i, 1], c=color[included_stations[i].line], label=f'{included_stations[i].__str__()}')
        plt.text(X_iso[i, 0], X_iso[i, 1], f'{included_stations[i].__str__()}', fontsize=4, ha='right', va='bottom')
    plt.title('Isomap Subway Map')
    plt.show()
    print(find_path(graph, find_stations_exact(substations, "O", 451), find_stations_exact(substations, "O", 362),
                    cost_func=cost_func))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
