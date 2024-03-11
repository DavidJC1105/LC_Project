import time
import matplotlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

waste = 0
counter = 0
percent = 0
percentage = 0

cred = credentials.Certificate("C:/Users/18DCummins.ACC/Downloads/lc-project-457ba-firebase-adminsdk-fwptw-0e086bdeef.json")
firebase_admin.initialize_app(cred,{'databaseURL': 'https://lc-project-457ba-default-rtdb.europe-west1.firebasedatabase.app/'})
#whatif = input('Enter 1 if you want to see your best sessions(What if #1) or enter 2 if you want to see your worst(What if #2). If you dont enter either of these you will be shown your best results: ')
#if whatif != '1' and whatif !='2':
 #   whatif = 1
#whatif = int(whatif)
#ref.update({'study_time':''})

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
'''
# Push data to Firebase
for data_point in custom_timestamps:
    timestamp = data_point["timestamp"]
    data = data_point["data"]
    ref.child('study_time').child(str(timestamp)).update(data)
'''

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

#ref.update({'study_time':''})
ref = db.reference().child('study_time')
data = ref.order_by_child('Location').get()
#print (type(data))
wasteminutes = []
totaltime = []
location = []
times = []
count = 0
'''
for timestamp, session_data in data.items():
    timestamp = int(timestamp)
    formatted_timestamp = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S %d-%m-%Y')
    print("At this time and date, this was the data for your study session: ", formatted_timestamp)
    
    for key, value in session_data.items():
        print(key, "is:", value)
    
    print("\n")
'''

for key,value in data.items():
    if value['Location'] not in location:
        location.append(value['Location'])
for i in range(len(location)):
    #times.append(0)
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
    #print(value['Location'])
    #wasteminutes.append(value['Wasted_Time(minutes)'])
    #totaltime.append(value['study_time(minutes)'])
   
#print(location)
#print(wasteminutes)
dl =0
#times[dl:len(wasteminutes)] = []
#print(times)
#print(totaltime)
study_time_ref = ref.child('study_time')

# Get all child nodes under the study_time node
time_nodes = study_time_ref.get()

# List to store study_time(minutes) values
study_time_minutes_list = []

# Iterate over each child node
if time_nodes:
    for time_node_key, time_node_data in time_nodes.items():
        # Check if the node has study_time(minutes) field
        if 'study_time(minutes)' in time_node_data:
            study_time_minutes_list.append(time_node_data['study_time(minutes)'])

print("Study time(minutes) values:", study_time_minutes_list)
lowest_value = wasteminutes[0]

for num in wasteminutes:
    # If the current number is lower than the lowest_value, update lowest_value
    if num < lowest_value:
        lowest_value = num
        
#print(lowest_value)       
totalwaste = []
for key, value in data.items():
    wastedtime = value.get('Wasted_Time(minutes)')
    if wastedtime is not None:
        totalwaste.append(wastedtime)

#print(totalwaste)
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

#print(totalminutes)
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


def find_lowest_time_and_waste(totalwaste, times):
    min_total_waste = min(totalwaste)  # Find the minimum total waste
    lowest_times = []  # Initialize a list to store all times with the lowest total waste

    # Iterate through the totalwaste list
    for index, waste in enumerate(totalwaste):
        if waste == min_total_waste:  # If the current total waste is equal to the minimum
            lowest_times.append(times[index])  # Add the corresponding time to the list

    # Return the list of times and the minimum total waste
    return lowest_times, min_total_waste


lowest_times, lowest_total_waste = find_lowest_time_and_waste(totalwaste, times)

def find_highest_time_and_waste(totalwaste, times):
    max_total_waste = max(totalwaste)  # Find the minimum total waste
    highest_times = []  # Initialize a list to store all times with the lowest total waste

    # Iterate through the totalwaste list
    for index, waste in enumerate(totalwaste):
        if waste == max_total_waste:  # If the current total waste is equal to the minimum
            highest_times.append(times[index])  # Add the corresponding time to the list

    # Return the list of times and the minimum total waste
    return highest_times, max_total_waste


highest_times, max_total_waste = find_highest_time_and_waste(totalwaste, times)


#print(lowest_total_waste)
mintimes = []
for timestamp in lowest_times:
    timestamp_value = float(timestamp)  # Convert timestamp to float
    study_time = data[timestamp]['study_time(minutes)']  # Fetch corresponding study time
    #formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_value))  # Format timestamp
    mintimes.append(study_time)
    #print("At", timestamp, "the study time was", study_time, "minutes.")

Location_interpret_min = []
for spot in lowest_times:
    spot_value = float(spot)  # Convert timestamp to float
    study_spot = data[spot]['Location']  # Fetch corresponding study time
    #formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_value))  # Format timestamp
    Location_interpret_min.append(study_spot)
    #print("At", timestamp, "the study time was", study_time, "minutes.")

#print(lowest_times)
#print(Location_interpret_min)

maxtimes = []
for timestamp in highest_times:
    timestamp_value = float(timestamp)  # Convert timestamp to float
    study_time = data[timestamp]['study_time(minutes)']  # Fetch corresponding study time
    #formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_value))  # Format timestamp
    maxtimes.append(study_time)
    #print("At", timestamp, "the study time was", study_time, "minutes.")

#print(maxtimes)

allmaxtimes = []
for timestamp in times:
    timestamp_value = float(timestamp)  # Convert timestamp to float
    study_time = data[timestamp]['study_time(minutes)']  # Fetch corresponding study time
    #formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_value))  # Format timestamp
    allmaxtimes.append(study_time)
    #print("At", timestamp, "the study time was", study_time, "minutes.")

#print(allmaxtimes)

maxtimes_spot = []
for spots in highest_times:
    spots_value = float(spot)  # Convert timestamp to float
    study_time = data[spots]['Location']  # Fetch corresponding study time
    #formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_value))  # Format timestamp
    maxtimes_spot.append(study_time)
    #print("At", timestamp, "the study time was", study_time, "minutes.")

#print(maxtimes_spot)

Location_interpret_max = []
for spot in highest_times:
    spot_value = float(spot)  # Convert timestamp to float
    study_spot = data[spot]['Location']  # Fetch corresponding study time
    #formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_value))  # Format timestamp
    Location_interpret_max.append(study_spot)
    #print("At", timestamp, "the study time was", study_time, "minutes.")
#
#print(Location_interpret)
#print(type(lowest_times))
#print("The time(s) with the lowest total waste is:", lowest_times)
#print("The corresponding total waste is:", lowest_total_waste)
ind = 0
starttime = []
for start in mintimes:
    start = int(mintimes[ind])
    starttime.append(start*60)
    ind = ind+1
    if ind == len(mintimes):
        break
#print (starttime)

ind_max=0
starttime_max = []
for start in maxtimes:
    start = int(maxtimes[ind_max])
    starttime_max.append(start*60)
    ind_max = ind_max+1
    if ind == len(maxtimes):
        break
#print (starttime)

formatted_times = []  # Initialize a list to collect formatted times

starting = 0
for eachtime in lowest_times:
    eachtime = int(eachtime) - starttime[starting]  # Assuming starttime is another list
    formatted_time = datetime.fromtimestamp(eachtime).strftime('%H:%M:%S')
    formatted_times.append(formatted_time)  # Collect formatted time in the list
    starting += 1

formatted_times_max = []  # Initialize a list to collect formatted times
'''
starting_max = 0
for eachtime in highest_times:
    eachtime = int(eachtime) - starttime_max[starting_max]  # Assuming starttime is another list
    formatted_time_max = datetime.fromtimestamp(eachtime).strftime('%H:%M:%S')
    formatted_times_max.append(formatted_time_max)  # Collect formatted time in the list
    starting_max += 1
'''
starting_max = 0
formatted_times_max = []  # Initialize an empty list to collect formatted times

for eachtime in highest_times:
    eachtime = int(eachtime) - starttime_max[starting_max % len(starttime_max)]  # Use modulo to ensure index wraps around
    formatted_time_max = datetime.fromtimestamp(eachtime).strftime('%H:%M:%S')
    formatted_times_max.append(formatted_time_max)  # Collect formatted time in the list
    starting_max += 1

# Print or use formatted_times_max as needed
#print(formatted_times_max)

from datetime import datetime


def date_to_words(highest_times):
    date_words = []
    for timestamp in highest_times:
        # Convert timestamp to integer
        timestamp_int = int(timestamp)
        
        # Convert timestamp to datetime object
        date_object = datetime.fromtimestamp(timestamp_int)
    
        # Convert datetime object to words
        date_word = date_object.strftime('%B %d, %Y')
        date_words.append(date_word)
    
    return date_words

date_words = date_to_words(highest_times)
#print(date_words)

def date_to_words_2(lowest_times):
    date_words_2 = []
    for timestamp in lowest_times:
        # Convert timestamp to integer
        timestamp_int = int(timestamp)
        
        # Convert timestamp to datetime object
        date_object = datetime.fromtimestamp(timestamp_int)
    
        # Convert datetime object to words
        date_word = date_object.strftime('%B %d, %Y')
        date_words_2.append(date_word)
    
    return date_words_2

date_words_2 = date_to_words_2(lowest_times)
#print(date_words_2)
def find_highest_percentage_values(times, totalwaste):
    # Initialize variables to store the highest percentage and its corresponding values
    highest_percentage = 0
    highest_values = []
    
    # Iterate through the lists
    for i in range(len(times)):
        # Cast times to float before division
        time_float = float(times[i])
        
        # Calculate the percentage of waste for the current entry
        percentage = (totalwaste[i] / time_float) * 100
        
        # If the current percentage is higher than the highest percentage, update the highest percentage
        # and reset the list of highest values
        if percentage > highest_percentage:
            highest_percentage = percentage
            highest_values = [(times[i], totalwaste[i])]
        # If the current percentage is equal to the highest percentage, append the pair to the list
        elif percentage == highest_percentage:
            highest_values.append((times[i], totalwaste[i]))
    
    # Return the highest percentage and its corresponding values
    return highest_percentage, highest_values

highest_percentage, highest_values = find_highest_percentage_values(allmaxtimes, totalwaste)
print("The highest percentage of waste is:", highest_percentage)
print("The values corresponding to the highest percentage of waste are:", highest_values)


def find_highest_percentage_time(times, totalwaste, highest_values):
    # Initialize variables to store the highest percentage and its corresponding time
    highest_percentage = 0
    highest_time = None
    
    # Iterate through the highest values
    for value_pair in highest_values:
        # Extract time and totalwaste from the value pair
        time_value, totalwaste_value = value_pair
        
        # Find the index of the value pair in the original lists
        index = totalwaste.index(totalwaste_value)
        
        # Get the corresponding time
        time = times[index]
        
        # Calculate the percentage of waste for the current entry
        percentage = (totalwaste_value / float(time)) * 100
        
        # Update the highest percentage and its corresponding time if applicable
        if percentage > highest_percentage:
            highest_percentage = percentage
            highest_time = time
    
    # Return the highest percentage and its corresponding time
    return  highest_time

highest_time = find_highest_percentage_time(times, totalwaste, highest_values)
highest_time = float(highest_time)
highest_time_datetime = datetime.fromtimestamp(highest_time)
print("The time corresponding to the highest percentage of waste is:", highest_time_datetime)


maxpercent = []
a=0
for x in maxtimes:
    x= maxtimes[a]
    maxi = (max_total_waste/x)*100
    maxi_rounded = round(maxi,2)
    maxpercent.append(maxi_rounded)
    a = a+1
    if a == len(maxtimes):
        break
'''
# Print the collected formatted times
def print_study_sessions_summary(formatted_times, date_words, locations, lowest_total_waste, mintimes):
   
    print("The modal shows that these were the most engaging and least stress inducing study sessions and they took place at these times in these locations:")
    time_place = 0
    inde = 0
    while time_place != len(formatted_times):
        print('On',date_words_2[inde],' at ',formatted_times[inde],' in ',Location_interpret_min[inde],'and you only wasted ',lowest_total_waste,'out of the total ',mintimes[inde],'minute(s)')
        inde = inde+1
        time_place = time_place+1

    print('To optimise your future study sessions to maximise engagement and minimise stress, my model recommends your have your study sessions in these locations')


print_study_sessions_summary(formatted_times, date_words, location, lowest_total_waste, mintimes)

print('\n')
def print_stress_inducing_sessions_summary(formatted_times_max, date_words, Location_interpret_max, max_total_waste, maxtimes):
    
    print("The model shows that these were the most stress inducing study sessions and they took place at these times in these locations:")
    time_place_max = 0
    inde_max = 0
    while time_place_max != len(formatted_times_max):
        print('On',date_words[inde_max],' at ',formatted_times_max[inde_max],' in ',Location_interpret_max[inde_max],'and you wasted ',max_total_waste,'out of the total of ',maxtimes[inde_max],'minute(s)')
        inde_max = inde_max+1
        time_place_max = time_place_max+1

    print('The model recommends for the future that you avoid these locations in order to minimise stress induction and maximise engagement while studying because in these locations you wasted:')


print_stress_inducing_sessions_summary(formatted_times_max, date_words, Location_interpret_max, max_total_waste, maxtimes)

b = 0
for y in maxpercent:
    print(maxpercent[b],'% of your time studying in ',Location_interpret_max[b])
    b=b+1
    if b == len(maxpercent):
        break
'''    
#print(totaltime)
#print(wasteminutes)
'''
import matplotlib.pyplot as plt
import numpy as np

# data from https://allisonhorst.github.io/palmerpenguins/
if whatif == 1:
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

if whatif == 2:
    plt.figure(figsize=(10, 6))
    plt.bar(Location_interpret_max, maxtimes, color='skyblue')

# Add a horizontal line for max_total_waste
    plt.axhline(y=max_total_waste, color='red', linestyle='--', label=f'Max Total Waste: {max_total_waste}')

# Add labels and title
    plt.xlabel('Location')
    plt.ylabel('Total Time Wasted (minutes)')
    plt.title('Total Time Wasted per Study Session')

# Add text annotation for each bar
    for i, v in enumerate(maxtimes):
        plt.text(i, v + 5, str(v), ha='center', va='bottom')

    plt.legend()
    plt.show()
'''