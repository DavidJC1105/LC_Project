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

cred = credentials.Certificate("C:/Users/18DCummins.ACC/Downloads/lc-project-457ba-firebase-adminsdk-fwptw-66b88dfdcc.json")
firebase_admin.initialize_app(cred,{'databaseURL': 'https://lc-project-457ba-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference()
#ref.update({'study_time':''})
ref = db.reference().child('study_time')
#source = input("Please input the study location: ")
data = ref.order_by_child('Location').get()
#print (type(data))
wasteminutes = []
totaltime = []
location = []
times = []
count = 0

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
    times.append(0)
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
times[dl:len(wasteminutes)] = []
#print(times)
#print(totaltime)
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
totalminutes = []
for key, value in data.items():
    totaltimes = value.get('study_time(minutes)')
    if totaltimes is not None:
        totalminutes.append(totaltimes)     

#print(totalminutes)


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

mintimes = []
for timestamp in lowest_times:
    timestamp_value = float(timestamp)  # Convert timestamp to float
    study_time = data[timestamp]['study_time(minutes)']  # Fetch corresponding study time
    #formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_value))  # Format timestamp
    mintimes.append(study_time)
    #print("At", timestamp, "the study time was", study_time, "minutes.")

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

formatted_times = []  # Initialize a list to collect formatted times

starting = 0
for eachtime in lowest_times:
    eachtime = int(eachtime) - starttime[starting]  # Assuming starttime is another list
    formatted_time = datetime.fromtimestamp(eachtime).strftime('%H:%M:%S')
    formatted_times.append(formatted_time)  # Collect formatted time in the list
    starting += 1

# Print the collected formatted times
print("You started your best study sessions at these times:")
for time in formatted_times:
    print(time)



        

import matplotlib.pyplot as plt
import numpy as np

# data from https://allisonhorst.github.io/palmerpenguins/

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
