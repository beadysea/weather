import weather_station
from msvcrt import kbhit, getch

def main():
    
    get_sample = False
    screen = False
    command = ''

    ws = weather_station(port)

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
            if time.time() >= ws.next_sample_time or ws.first_run:

                data = ws.get_sample()
                ws.write_file(data)

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
