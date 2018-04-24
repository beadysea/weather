import time
import serial
from msvcrt import kbhit, getch
import os

def main():
    file_dir = r'.\weather_logs'
    get_sample = False
    screen = False
    calibration = -2
    command = ''

    clear_screen()
    header()
    coms_instruction()
    valid_port = False
    while not valid_port:
        try:
            port = int(input('port number = '))
        except ValueError:
            print('No valid port number entered, please try again')
            valid_port = False
        else:
            try:
                if port > -1:
                    valid_port = True
                else:
                    raise ValueError
            except ValueError:
                print('Port number entered is invalid, please try again')
                valid_port = False
            else:
                valid_port = True


    clear_screen()
    header()
    file_instruction()

    file_prefix = input('File Prefix: ')
    if file_prefix == '':
        default_file = True
    else:
        default_file = False
        fp = '{}/{}'.format(file_dir,file_prefix)

    clear_screen()
    header()
    aquisition_instruction()

    valid_hours = False
    while not valid_hours:
        try:
            aq_hours = int(input('Hours: '))
        except ValueError:
            print('No valid number entered, please try again')
            valid_hours = False
        else:
            try:
                if aq_hours > -1:
                    valid_hours = True
                else:
                    raise ValueError
            except ValueError:
                print('Number of hours entered is invalid, please try again')
                valid_hours = False
            else:
                valid_hours = True

    valid_minutes = False
    while not valid_minutes:
        try:
            aq_minutes = int(input('Minutes: '))
        except ValueError:
            print('No valid number entered, please try again')
            valid_minutes = False
        else:
            try:
                if aq_minutes > -1:
                    valid_minutes = True
                else:
                    raise ValueError
            except ValueError:
                print('Number of minutes entered is invalid, please try again')
                valid_minutes = False
            else:
                valid_minutes = True

    valid_seconds = False
    while not valid_seconds:
        try:
            aq_seconds = int(input('Seconds: '))
        except ValueError:
            print('No valid number entered, please try again')
            valid_seconds = False
        else:
            try:
                if aq_seconds > -1:
                    valid_seconds = True
                else:
                    raise ValueError
            except ValueError:
                print('Number of seconds entered is invalid, please try again')
                valid_seconds = False
            else:
                valid_seconds = True

    sample_delay = sample_interval(aq_hours, aq_minutes, aq_seconds)

    clear_screen()
    header()
    use_instruction()

    first_run = True
    next_sample_time = time.time()
    # start the main loop
    while command != 'quit':
        command = kbd_scan()
        if command == 'quit':
            break
        if command == 'toggle_screen_print':
            if not screen:
                screen = True
                line_count = 0
            else:
                screen = False
                line_count = 0
                clear_screen()
                header()
                use_instruction()

        if command == 'toggle_sample':
            if get_sample == False:
                get_sample = True
            else:
                get_sample = False
                first_run = True

        if get_sample:
            if time.time() >= next_sample_time or first_run:
                ser = com_open(port) #Open a serial comm link
                if ser == -1:
                    #com port failure
                    command = 'quit'
                    break
                #Sample Data and Time
                t_struct = ('Y', 'm', 'd', 'H', 'M', 'S')
                data ={t:time.strftime('%{}'.format(t)) for t in t_struct}

                # set next sample time ready for next loop
                next_sample_time = time.time() + sample_delay + calibration

                #send a byte to weather station triggering sampling of sensors
                out_byte = '1'
                ser.write(out_byte.encode())

                # read newest data from Arduino weather station
                rcvd = str(ser.readline(), 'utf8').strip('\r\n')
                ser.close() #Close the serial com link
                rcv_struct = ('t', 'p', 'h')
                rcvdata = rcvd.split(',')
                data.update({rc:rcvdata[rcv_struct.index(rc)]
                            for rc in rcv_struct})

                #build the Filename using logtime
                filetime = '{}-{}-{}_{}-{}-{}'.format(
                                                data['Y'], data['m'], data['d'],
                                                data['H'], data['M'], data['S']
                                                )
                #build the date field
                datefield = '{}/{}/{}'.format(data['d'], data['m'], data['Y'])

                #build the ti[][me field
                timefield = '{}:{}:{}'.format(data['H'], data['M'], data['S'])

                if first_run:
                    # create log file
                    if default_file:
                        file_path =r'{}\{}.csv'.format(file_dir, filetime)
                    else:
                        file_path = fp + '_{}.csv'.format(filetime)
                    if not os.path.exists(file_dir):
                        os.mkdir(file_dir)
                    with open(file_path,'x') as file:
                        file.write('Date,Time,Temperature \u00b0C,Pressure Pa,Humidity %\n')
                    file.close()
                    first_run = False
                #write to log file
                with open(file_path, 'a') as file:
                    file.write('{},{},{},{},{}\n'.format(
                                                datefield, timefield,
                                                data['t'], data['p'], data['h']
                                                ))
                    file.close()

                # Printing to screen
                if screen:
                    if line_count == 0:
                        clear_screen()
                        print('Time\t\tTemperature \u00b0C\tPressure Pa\tHumidity %')
                        line_count += 1
                    if line_count < 26:
                        print('{}\t{}\t\t{}\t\t{}'.format(
                                                    timefield, data['t'],
                                                    data['p'], data['h']
                                                    ))
                        line_count += 1
                    else:
                        clear_screen()
                        print('Time\t\tTemperature \u00b0C\tPressure Pa\tHumidity %')
                        print('{}\t{}\t\t{}\t\t{}'.format(
                                                    timefield, data['t'],
                                                    data['p'], data['h']
                                                    ))
                        line_count = 2


# Other Functions
def com_open(port):
    """Open a communication link to the Arduino weather station

        Args:
            port: The COM port to open
        """
    ser_dev = '\\\\.\\COM{}'.format(port)

    # Establish the connection on a specific port
    try:
        ser = serial.Serial(ser_dev, 9600)
    except serial.serialutil.SerialException:

        print('Fatal Error: Com port {} could not be opened.'.format(port))
        print('Terminating the application, please restart the application.')
        ser = -1
        return ser
    else:
        time.sleep(2)
        return ser

def sample_interval(hours, minutes, seconds):
    """Sets the interval between data samples

    Args:
    hours - the hours between data samples 0 and 23
    minutes - integer between 0 and 59
    seconds - integer between 0 and 59

    Returns:
    time interval in seconds.
    """
    if hours == 0 and minutes == 0 and seconds == 0:
        interval_seconds = 60  # default interval of 1 minute
    else:
        interval_seconds = hours * 3600 + minutes * 60 + seconds
    return interval_seconds

def kbd_scan():
    """Scans keyboard for valid keypresses

    Args:
    none

    Return:
    a user command string
    """
    cmd = ''
    if kbhit():
        unichr = ord(getch())
        if unichr != 0xe0:
            asciichr = chr(unichr).lower()
        if asciichr == ' ':
            cmd = 'toggle_sample'
        if asciichr == 'q':
            cmd = 'quit'
        if asciichr == 'p':
            cmd = 'toggle_screen_print'
        return cmd

def header():
    """Prints application header text to the console
    """
    print('''
    Weather Logger
    --------------
    This program creates a csv logfile of weather data obtained from the
    arduino weather station.

    ''')
    return

def coms_instruction():
    """Prints communication setup instructions to the console
    """

    print('''
    Arduino Communications settings
    -------------------------------

    To communicate with the arduino we need to know the COM port it is attached
    to. You can find this by looking at the bottom right of your arduino
    development environment window.

    Enter the com port number below and press return.

    ''')
    return

def file_instruction():
    """Prints log file setup instructions to the console
    """

    print('''
    Weather Log File
    ----------------

    The weather log files are automatically created and saved in the
    weather_logs folder located in the same folder as this python file.

    The default filename given to log files is the date and time at the start
    of data aquisition in the form yyyy-mm-dd_hh-mm-ss.csv.

    To add a prefix to the filename, enter the prefix below and press return.
    To keep the default filename press return.

    ''')
    return

def aquisition_instruction():
    """Prints aquisition setup instructions to the console
    """

    print('''
    Weather Data Aquistion
    ----------------------

    Weather data is sampled every minute by default.

    To change the sample interval enter the hours, minutes and seconds
    you want to wait between each sample.
    ''')
    return

def use_instruction():
    """Prints user instructions to the console
    """

    print('''
    Weather Logger controls
    -----------------------

    Use the following keys to control the weather logger.

    Spacebar - Start/Stop data logging

    P - start/stop printing data to the screen

    Q - Quit
    ''')
    return

def clear_screen():
    """Clears the console clear_screen
    """

    os.system('cls')
    return

if __name__ == '__main__':
    main()
