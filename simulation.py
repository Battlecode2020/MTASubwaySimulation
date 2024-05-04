import pandas as pd

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

def movement(time):
    leaving_dict = locations_leaving("MTA_Subway_Hourly_Ridership.csv", time)
    returning_dict = locations_leaving("MTA_Subway_Hourly_Ridership.csv", time)

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
transit_timestamp: time EX: 11/06/2022 12:00:00 AM

station_complex_id: complex

ridership

'''