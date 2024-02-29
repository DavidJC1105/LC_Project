import time
import matplotlib
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

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
print (data)
wasteminutes = []
totaltime = []
location = []
count = 0
for key,value in data.items():
    if value['Location'] not in location:
        location.append(value['Location'])
for i in range(len(location)):
    wasteminutes.append(0)
    totaltime.append(0)
for key,value in data.items():
    if value['Location'] == location[count]:
        wasteminutes[count]+=value['Wasted_Time(minutes)']
        totaltime[count]+=value['study_time(minutes)']
    else:
        count = count + 1
        wasteminutes[count]+=value['Wasted_Time(minutes)']
        totaltime[count]+=value['study_time(minutes)']
    print(value['Location'])
    #wasteminutes.append(value['Wasted_Time(minutes)'])
    #totaltime.append(value['study_time(minutes)'])
   
print(location)
print(wasteminutes)
print(totaltime)
import matplotlib.pyplot as plt
import numpy as np

# data from https://allisonhorst.github.io/palmerpenguins/

study_space = location
amountoftime = {
    "Below": wasteminutes,
    "Above": totaltime,
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(len(location))

for boolean, amountoftime in amountoftime.items():
    p = ax.bar(study_space, amountoftime, width, label=boolean, bottom=bottom)
    bottom += amountoftime

ax.set_title("Number of penguins with above average body mass")
ax.legend(loc="upper right")

plt.show()