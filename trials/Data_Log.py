#Arduino Weather Station CSV Data Logging
import csv
import serial
import os
import time
from msvcrt import kbhit, getch
from time import sleep

#_________________________Functions____________________________#

def takeReading():
    data = str(ser.readline().strip(), 'utf-8')
    sensorData = data.split()
    return sensorData

#populateFile() opens the .csv file specified by the file_name and appends information from the arduino.
def populateFile(file_name):
    with open ("C:/Users/arran/OneDrive/Documents/Weather Station Data/" + file_name, 'a') as csv_file:
        sensorData = takeReading()
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([sensorData[0],sensorData[1], sensorData[2], sensorData[3], sensorData[4]])

def kbdScan(Command):
    if kbhit():
        unichr = ord(getch())
        if unichr != 0xe0:
            asciichr = chr(unichr).lower()
        if asciichr == ' ':
            Command = 'STOP'
        if asciichr == 'q':
            Command = 'quit'
        if asciichr == 'p':
            Command = 'toggle_screen_print'
    return Command

#csvSetUp()
def csvSetUp():
    with open ("C:/Users/arran/OneDrive/Documents/Weather Station Data/" + file_name, 'a') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Weather Station Project"])
                csv_writer.writerow(["Day","Hour","Temperature","Pressure","Humidity","\n"])
    return file_name
#_____________________Program Introduction_______________________________#

print("Initializing....\n")
COM = input("Please input the COM port your Arduino is currently using ")
ser = serial.Serial('COM'+COM, 9600) # Establish the connection on a specific port
sleep(2)

print ("\nThis software logs data for the Arduino Weather Station project \nand allows files to be created then written to and/or open files and append to them.\n")

#________________________Main Program___________________________________#

#Each time the program a command is entered and the process finishes the program returns to this point to request another Command
#from the user.
get_sample = False
screen = False
first_run = True
main = True


while main == True:
    print(first_run)
    Command = input("Type commands here all in upper-case (Type HELP for a list of commands): ")
    while Command == "RUN":
        Command = kbdScan(Command)
        sleep (5)
        if Command == "STOP":
            first_run = True
            break
        if first_run == True:
            New_Old = input("Would you like to create a new file? ")
            if New_Old == "YES":
                #defFile is the name of the file the user would like to create
                defFile = input("Enter the file name that you would like to use: ")
                #File_name is the UserDef variable combined with .csv
                file_name = defFile+".csv"
                first_run = False
                csvSetUp()
            elif New_Old == "NO":
                file_name = input("Please type the file name exactly followed by .csv: ")
                populateFile(file_name)
            else:
                print("Invalid command please answer YES or NO: ")
        if first_run == False:
            populateFile(file_name)
            print("Press Space at any time to end sample")
        #Prints list of the commands availabe
    if Command == "READ":
        sensorData = takeReading()
        print ("Temperature       Pressure         Humidity")
        print (sensorData)
    if Command == "HELP":
        print("RUN Starts the program, or continues it if it has been paused. READ takes an instant reading. EXIT exits the program.")
        #Pauses the program
    if Command == "EXIT":
        main = False

print("Program Exiting...")
sleep(5)
