import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import serial

ser = serial.Serial()
ser.baudrate = 115200
ser.port = "COM8"
ser.open()
waste = 0
counter = 0

cred = credentials.Certificate("C:/Users/18DCummins.ACC/Downloads/lc-project-457ba-firebase-adminsdk-fwptw-7685537f36.json")
firebase_admin.initialize_app(cred,{'databaseURL': 'https://lc-project-457ba-default-rtdb.europe-west1.firebasedatabase.app/'})
ref = db.reference()
ref.update({'study_time':''})
ref = db.reference().child('study_time')
source = input("Please input the study location: ")
while True:
    mb_one = str(ser.readline().decode('utf-8'))
    mb_one = mb_one.replace(" ","")
    mb_one = mb_one.replace("\r\n","")
    number = mb_one
    numb = int(number)
    if numb==0:
        waste = waste + 1
    if numb==1:
        counter = counter + numb
    numb = str(numb)
    print("You have been studying for ",counter," minute/s and you have wasted ",waste," of those minute/s")
    if numb.isdigit():
        ref.update({str(int(time.time())):{'study_time':counter, 'Location':source, 'Wasted_Time':waste}})
    else:
        print("There has been an error")