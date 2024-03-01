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
#print (data)
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
print(wasteminutes)
dl =0
times[dl:len(wasteminutes)] = []
print(times)
#print(totaltime)
lowest_value = wasteminutes[0]

for num in wasteminutes:
    # If the current number is lower than the lowest_value, update lowest_value
    if num < lowest_value:
        lowest_value = num
        
print(lowest_value)       
totalwaste = []
for key, value in data.items():
    wastedtime = value.get('Wasted_Time(minutes)')
    if wastedtime is not None:
        totalwaste.append(wastedtime)

print(totalwaste)       
        
        
        
        
        
        

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