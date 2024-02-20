import serial
import time

ser = serial.Serial()
ser.baudrate = 115200
ser.port = "COM8"
ser.open()
counter = 0
waste = 0

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
    print("You have been studying for ",counter," minute/s and you have wasted ",waste," of those minute/s")