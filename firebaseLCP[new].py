import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import serial

ser = serial.Serial()
ser.baudrate = 115200
ser.port = "COM9"
ser.open()
waste = 0
counter = 0
percent = 0
percentage = 0

cred = credentials.Certificate("C:/Users/18DCummins.ACC/Downloads/lc-project-457ba-firebase-adminsdk-fwptw-7685537f36.json")
firebase_admin.initialize_app(cred,{'databaseURL': 'https://lc-project-457ba-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference()
#ref.update({'study_time':''})
ref = db.reference().child('study_time')
source = input("Please input the study location: ")
while True:
    mb_one = str(ser.readline().decode('utf-8'))
    mb_one = mb_one.replace(" ","")
    mb_one = mb_one.replace("\r\n","")
    number = mb_one
    number1 = number[0]
    numb = int(number1)
    if numb==0:
        waste = waste + 1
        percent = (waste/counter)*100
        mup = str(percent)
        yas = mup[0:5]
        percentage = float(yas)
    if numb==1:
        counter = counter + numb
        percent = (waste/counter)*100
        mup = str(percent)
        yas = mup[0:5]
        percentage = float(yas)
        print("You have been studying for ",counter," minute(s) and you have wasted ",percentage," of those minute(s)",counter,',',waste)
    numb = str(numb)
    if numb.isdigit():
        ref.update({str(int(time.time())):{'study_time(minutes)':counter, 'Location':source, 'Wasted_Time(minutes)':waste}})
    else:
        print("There has been an error")