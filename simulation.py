import pandas as pd
import numpy as np
import random

def increment_hour(hour):
    if hour == "01":
        return "02"
    elif hour == "02":
        return "03"
    elif hour == "03":
        return "04"
    elif hour == "04":
        return "05"
    elif hour == "05":
        return "06"
    elif hour == "06":
        return "07"
    elif hour == "07":
        return "08"
    elif hour == "08":
        return "09"
    elif hour == "09":
        return "10"
    elif hour == "10":
        return "11"
    elif hour == "11":
        return "12"
    elif hour == "12":
        return "01"
    else:
        raise Exception

def nextTime(time):
    next_time = ""
    parts = time.split(" ")
    if parts[1] == "11:00:00" and parts[2] == "PM":
        dates = parts[0].split("/")
        dates[1] = int(dates[1]) + 1
        next_time = dates[0].__str__() + "/" +  dates[1].__str__() + "/" + dates[2].__str__() + " 12:00:00 AM"
    elif parts[1] == "11:00:00" and parts[2] == "AM":
        next_time = parts[0] + " 12:00:00 PM"
    else:
        timeParts = parts[1].split(":")
        next_time = parts[0] + " " + increment_hour(timeParts[0]) + ":" + timeParts[1] + ":" + timeParts[2] + " " + parts[2]
    return next_time
def locations_leaving(filename, time):
    df = pd.read_csv(filename)
    condition = df['transit_timestamp'] == time
    result = df[condition]
    complex_dict = {}
    for index,row in result.iterrows():
        if row['station_complex_id'] in complex_dict:
            complex_dict[row['station_complex_id']] += row['ridership']
        else:
            complex_dict[row['station_complex_id']] = row['ridership']
    return complex_dict

def create_prob_array(dict):
    prob_array = []
    for key,value in dict.items():
        prob_array.extend(([key] * value))
    return prob_array

def movement(time):
    movement_matrix = np.zeros((640,640))
    leaving_dict = locations_leaving("MTAoct16-23EntryData.csv", time)
    arriving_dict = locations_leaving("MTAoct16-23EntryData.csv", nextTime(time))
    prob_array = create_prob_array(leaving_dict)
    for key,value in leaving_dict.items():
        for j in range(value):
            movement_matrix[key][random.choice(prob_array)] += 1
    return movement_matrix




'''
dict = locations_leaving("MTA_Subway_Hourly_Ridership.csv", "11/06/2022 04:00:00 AM")
print(dict[307])
max = 0
max_key = -1
for key, value in dict.items():
    if value > max:
        max = value
        max_key = key
print(max)
print(max_key)
'''


'''
curr_time = "10/16/2023 04:00:00 PM"
all_movement_matrix = []
for i in range(168):
    curr_time = nextTime(curr_time)
    all_movement_matrix.append(movement(curr_time))

'''


'''
transit_timestamp: time EX: 11/06/2022 12:00:00 AM

station_complex_id: complex

ridership

'''