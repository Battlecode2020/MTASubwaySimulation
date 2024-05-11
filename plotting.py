import matplotlib.pyplot as plt

def plot_subway_minutes_data():
    X_data = [i for i in range(1,25)]
    Y_data = [398160, 312798, 430527, 1404339, 2981002, 6736218, 13222875, 15240866, 9400772, 6075602, 5188142, 5421861, 6351244, 7735800, 9572866, 9436765, 10293274, 7658762, 4855372, 3382071, 2557574, 2313184, 1306603, 667276]
    plt.plot(X_data, Y_data)
    plt.xlabel('Hour on 24 Hour Clock')
    plt.ylabel('Total Minutes of Subway Travel')
    plt.title('Time of Day vs Subway Usage')
    plt.show()
plot_subway_minutes_data()