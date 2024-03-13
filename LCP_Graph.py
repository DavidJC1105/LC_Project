import time
import matplotlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
waste = 0
counter = 0
percent = 0
percentage = 0
cred = credentials.Certificate("C:/Users/18DCummins.ACC/Downloads/lc-project-457ba-firebase-adminsdk-fwptw-0e086bdeef.json")
firebase_admin.initialize_app(cred,{'databaseURL': 'https://lc-project-457ba-default-rtdb.europe-west1.firebasedatabase.app/'})
while True:
    whatif = input('Enter 1 if you want to see your best sessions (What if #1) or enter 2 if you want to see your worst (What if #2) or enter 3 if you wish to see all you sessions and their times. If you don\'t enter either of these you will be shown your best results: ')
    if whatif in ['1', '2','3']:
        break
whatif = int(whatif)
custom_timestamps = [
    #Monday
    {"timestamp": 175795840, "data": {"Location": "Room 1", "Wasted_Time(minutes)": 10, "study_time(minutes)": 65}},
    {"timestamp": 175799480, "data": {"Location": "Room 4", "Wasted_Time(minutes)": 8, "study_time(minutes)": 30}},
    #Tuesday
    {"timestamp": 174906480, "data": {"Location": "Room 3", "Wasted_Time(minutes)": 15, "study_time(minutes)": 78}},
    {"timestamp": 174910800, "data": {"Location": "Room 2", "Wasted_Time(minutes)": 4, "study_time(minutes)": 95}},
    #Wednesday
    {"timestamp": 174915120, "data": {"Location": "Room 1", "Wasted_Time(minutes)": 13, "study_time(minutes)": 40}},
    {"timestamp": 174919440, "data": {"Location": "Room 5", "Wasted_Time(minutes)": 7, "study_time(minutes)": 37}},
    #Thursday
    {"timestamp": 174923760, "data": {"Location": "Room 5", "Wasted_Time(minutes)": 20, "study_time(minutes)": 92}},
    {"timestamp": 174928080, "data": {"Location": "Room 2", "Wasted_Time(minutes)": 16, "study_time(minutes)": 80}},
    #Friday
    {"timestamp": 174932400, "data": {"Location": "Room 3", "Wasted_Time(minutes)": 4, "study_time(minutes)": 25}},
    {"timestamp": 174936720, "data": {"Location": "Room 4", "Wasted_Time(minutes)": 14, "study_time(minutes)": 58}},
    #Saturday
    {"timestamp": 174941040, "data": {"Location": "Room 1", "Wasted_Time(minutes)": 6, "study_time(minutes)": 45}},
    {"timestamp": 174945360, "data": {"Location": "Room 5", "Wasted_Time(minutes)": 21, "study_time(minutes)": 34}},
    #Sunday
    {"timestamp": 174949680, "data": {"Location": "Room 3", "Wasted_Time(minutes)": 5, "study_time(minutes)": 87}},
    {"timestamp": 174954000, "data": {"Location": "Room 4", "Wasted_Time(minutes)": 21, "study_time(minutes)": 60}},
    # Add more custom timestamps and corresponding data as needed
]
ref = db.reference()
# Check if the study_time node already exists in the Firebase database
study_time_exists = ref.child('study_time').get() is not None
# If the study_time node does not exist, add it to the Firebase database
if not study_time_exists:
    # Define the study_time node
    study_time_ref = ref.child('study_time')
    # Add the data to the database
    study_time_ref.update({'': ''})  # Add an empty child to prevent overwriting
    print("study_time node added to the Firebase database.")
else:
    print("study_time node already exists in the Firebase database, skipping adding it again.")
# Check if the dataset already exists in the Firebase database
dataset_exists = ref.child('study_time').get() is not None
# If the dataset does not exist, add it to the Firebase database
if not dataset_exists:
    # Define the study_time node
    study_time_ref = ref.child('study_time')
    # Loop through custom_timestamps and update Firebase
    for data_point in custom_timestamps:
        timestamp = str(data_point["timestamp"])  # Convert timestamp to string
        data = data_point["data"]
        # Add the data to the database
        study_time_ref.child(timestamp).set(data)
        print(f"Data added for timestamp: {timestamp}")
    print("Data update complete.")
else:
    print("Dataset already exists in the Firebase database, skipping adding it again.")
ref = db.reference().child('study_time')
data = ref.order_by_child('Location').get()
wasteminutes = []
totaltime = []
location = []
times = []
count = 0
if whatif == 3:
    for timestamp, session_data in data.items():
        timestamp = int(timestamp)
        formatted_timestamp = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S %d-%m-%Y')
        print("At this time and date, this was the data for your study session: ", formatted_timestamp)
        for key, value in session_data.items():
            print(key, "is:", value)
        print("\n")
for key,value in data.items():
    if value['Location'] not in location:
        location.append(value['Location'])
for i in range(len(location)):
    wasteminutes.append(0)
    totaltime.append(0)
for k,v in data.items():
    times.append(k)
for key,value in data.items():
    if value['Location'] == location[count]:
        wasteminutes[count]+=value['Wasted_Time(minutes)']
        totaltime[count]+=value['study_time(minutes)']
    else:
        count = count + 1
        wasteminutes[count]+=value['Wasted_Time(minutes)']
        totaltime[count]+=(value['study_time(minutes)']-value['Wasted_Time(minutes)'])       
totalwaste = []
for key, value in data.items():
    wastedtime = value.get('Wasted_Time(minutes)')
    if wastedtime is not None:
        totalwaste.append(wastedtime)    
totalwaste_average = 0
av = 0
index = 0
for x in totalwaste:
    av = av+x
    index = index+1
    if index == len(totalwaste):
        break
totalwaste_average = av/len(totalwaste)
wasteminutes.append(totalwaste_average)
totalminutes = []
for key, value in data.items():
    totaltimes = value.get('study_time(minutes)')
    if totaltimes is not None:
        totalminutes.append(totaltimes)     
totalminutes_average = 0
av2 = 0
index2 = 0
for x in totalminutes:
    av2 = av2+x
    index2 = index2+1
    if index2 == len(totalminutes):
        break
totalminutes_average = av2/len(totalminutes)
totaltime.append(totalminutes_average)
location.append('Average')
allmaxtimes = []
for timestamp in times:
    timestamp_value = float(timestamp)  # Convert timestamp to float
    study_time = data[timestamp]['study_time(minutes)']  # Fetch corresponding study time
    allmaxtimes.append(study_time)
def find_highest_percentage_values(times, totalwaste, allmaxtimes):
    # Initialize variables to store the highest percentage, its corresponding values, and corresponding times
    highest_percentage = 0
    highest_values = []
    highest_times = []
    # Iterate through the lists
    for i in range(len(times)):
        # Cast times to float before division
        time_float = float(times[i])
        # Calculate the percentage of waste for the current entry
        percentage = (totalwaste[i] / time_float) * 100
        # If the current percentage is higher than the highest percentage, update the highest percentage
        # and reset the lists of highest values and highest times
        if percentage > highest_percentage:
            highest_percentage = percentage
            highest_values = [(times[i], totalwaste[i])]
            highest_times = [allmaxtimes[i]]
        # If the current percentage is equal to the highest percentage, append the pair and time to the lists
        elif percentage == highest_percentage:
            highest_values.append((times[i], totalwaste[i]))
            highest_times.append(allmaxtimes[i])
    # Return the highest percentage, its corresponding values, and corresponding times
    return highest_percentage, highest_values, highest_times
highest_percentage, highest_values, highest_times = find_highest_percentage_values(allmaxtimes, totalwaste, times)
highest_percentage = format(highest_percentage, '.2f')
def find_lowest_percentage_values(times, totalwaste, allmaxtimes):
    # Initialize variables to store the highest percentage, its corresponding values, and corresponding times
    lowest_percentage = 100
    lowest_values = []
    lowest_times = []
    # Iterate through the lists
    for i in range(len(times)):
        # Cast times to float before division
        time_float = float(times[i])
        # Calculate the percentage of waste for the current entry
        percentage = (totalwaste[i] / time_float) * 100
        # If the current percentage is higher than the highest percentage, update the highest percentage
        # and reset the lists of highest values and highest times
        if percentage < lowest_percentage:
            lowest_percentage = percentage
            lowest_values = [(times[i], totalwaste[i])]
            lowest_times = [allmaxtimes[i]]
        # If the current percentage is equal to the highest percentage, append the pair and time to the lists
        elif percentage == lowest_percentage:
            lowest_values.append((times[i], totalwaste[i]))
            lowest_times.append(allmaxtimes[i])
    # Return the highest percentage, its corresponding values, and corresponding times
    return lowest_percentage, lowest_values, lowest_times
lowest_percentage, lowest_values, lowest_times = find_lowest_percentage_values(allmaxtimes, totalwaste, times)
lowest_percentage = format(lowest_percentage, '.2f')
def date_to_words_3(hightime):
    date_words_3 = []
    for timestamp in highest_times:
        # Convert timestamp to integer
        timestamp_int = int(timestamp)
        # Convert timestamp to datetime object
        date_object = datetime.fromtimestamp(timestamp_int)
        # Convert datetime object to words
        date_word = date_object.strftime('%m/%d/%Y %H:%M')
        date_words_3.append(date_word)
    return date_words_3
date_words_3 = date_to_words_3(highest_times)
def date_to_words_4(lowtime):
    date_words_4 = []
    for timestamp in lowest_times:
        # Convert timestamp to integer
        timestamp_int = int(timestamp)
        # Convert timestamp to datetime object
        date_object = datetime.fromtimestamp(timestamp_int)
        # Convert datetime object to words
        date_word = date_object.strftime('%m/%d/%Y %H:%M')
        date_words_4.append(date_word)
    return date_words_4
date_words_4 = date_to_words_4(lowest_times)
Location_interpret_max = []
for spot in highest_times:
    spot_value = float(spot)  # Convert timestamp to float
    study_spot = data[spot]['Location']  # Fetch corresponding study time
    Location_interpret_max.append(study_spot)
Location_interpret_min = []
for spot in lowest_times:
    spot_value = float(spot)  # Convert timestamp to float
    study_spot = data[spot]['Location']  # Fetch corresponding study time
    Location_interpret_min.append(study_spot)
total = []
waster = []
for numbers in highest_times:
    mins_value = data[numbers]['study_time(minutes)']
    mins_value_2 = data[numbers]['Wasted_Time(minutes)']
    total.append(mins_value)
    waster.append(mins_value_2)
total_2 = []
waster_2 = []
for numbers in lowest_times:
    mins_value = data[numbers]['study_time(minutes)']
    mins_value_2 = data[numbers]['Wasted_Time(minutes)']
    total_2.append(mins_value)
    waster_2.append(mins_value_2)
if whatif == 1:
    def print_waste_info(date_words_4, lowest_percentage, Location_interpret_min, total_2, waster_2):
        for i in range(len(total_2)):
            print('At', date_words_4[i], 'you wasted', lowest_percentage, '% of your time in', Location_interpret_min[i] + '.',
              'Out of your', total_2[i], 'minutes you spent studying, you wasted', waster_2[i], 'of them. This model recommends that if you wish to continue seeing similar results, to keep studying in these location(s) at these time(s)')

    print_waste_info(date_words_4, lowest_percentage, Location_interpret_min, total_2, waster_2)
if whatif == 2:
    def print_highest_waste_info(date_words_3, highest_percentage, Location_interpret_max, total, waster):
        for i in range(len(total_2)):
            print('At', date_words_3[i], 'you wasted', highest_percentage, '% of your time in', Location_interpret_max[i] + '.',
              'Out of your', total[i], 'minutes you spent studying, you wasted', waster[i], 'of them. This model recommends that for better results to avoid these location(s) at these time(s)')
    print_highest_waste_info(date_words_3, highest_percentage, Location_interpret_max, total, waster)
if whatif == 1:
    # Create subplots
    fig, ax = plt.subplots()
    # Width of each bar
    width = 0.35
    # Indices for each location
    ind = np.arange(len(date_words_4))
    # Plot the bars
    for i, (time, loc, total, waste) in enumerate(zip(date_words_4, Location_interpret_min, total_2, waster_2)):
        # Plot the first value (total time) in blue
        ax.bar(ind[i] - width/2, total, width, color='blue', label='Total Minutes' if i == 0 else None)
        # Plot the second value (wasted time) beside the first one in orange
        ax.bar(ind[i] + width/2, waste, width, color='orange', label='Wasted Minutes' if i == 0 else None)
        # Set x-axis labels including room and time
    x_labels = [f"{loc} ({time})" for time, loc in zip(date_words_4, Location_interpret_min)]
    ax.set_xticks(ind)
    ax.set_xticklabels(x_labels, rotation=45, ha='right')  # Rotate x-labels for better readability
    # Labeling
    plt.xlabel('Location (Time)')
    plt.ylabel('Minutes')
    plt.title('Wasted Time for Lowest Percentage Sessions')
    # Display legend outside the plot area
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
if whatif == 2:
# Plot the data
    fig, ax = plt.subplots()
# Width of each bar
    width = 0.35
# Indices for each location
    ind = np.arange(len(highest_values))
# Plot the bars
    for i, (value_pair, time) in enumerate(zip(highest_values, date_words_3)):
    # Plot the first value in blue
        ax.bar(ind[i] - width/2, value_pair[0], width, color='blue', label='Total Minutes' if i == 0 else None)
    # Plot the second value beside the first one in orange
        ax.bar(ind[i] + width/2, value_pair[1], width, color='orange', label='Wasted Minutes' if i == 0 else None)
# Set x-axis labels including room and time
    x_labels = [f"{loc} ({time})" for loc, time in zip(Location_interpret_max, date_words_3)]
    ax.set_xticks(ind)
    ax.set_xticklabels(x_labels)
# Labeling
    plt.xlabel('Location (Time)')
    plt.ylabel('Minutes')
    plt.title('Wasted Time for Highest Percentage Sessions')
# Display legend outside the plot area
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.show()
if whatif == 3:
    study_space = location
    amountoftime = {
        "The amount of wasted time": wasteminutes,
        "Total time spent studying": totaltime,
    }
    width = 0.5
    fig, ax = plt.subplots()
    bottom = np.zeros(len(location))
    for boolean, amountoftime in amountoftime.items():
        p = ax.bar(study_space, amountoftime, width, label=boolean, bottom=bottom)
        bottom += amountoftime
    ax.set_title("The ratio of wasted time in regards to total time in minutes spent studying")
    ax.legend(loc="upper right")
    plt.show()