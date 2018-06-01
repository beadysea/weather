import time, serial, os

class weather_station:

    def __init__(self, port = 0, sample_delay = 0):

        self._port = port
        self.file_dir = r'.\weather_logs'
        self.first_run = True
        self.next_sample_time = time.time()
        self.timefmt = ('Y', 'm', 'd', 'H', 'M', 'S')
        self.rvcdatafmt = ('t', 'p', 'h')
        self._sample_delay = sample_delay
        self.calibration = 0
        self.send_byte = '1'

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if value in range(0,256):
            self._port = value
        else:
            raise ValueError('Port number outside valid range of 0 to 255')

    @property
    def sample_delay(self):
        return self._sample_delay

    @sample_delay.setter
    def sample_delay(self, hours, minutes, seconds):
        """Sets the delay between data samples

        Args:
        hours - the hours between data samples 0 and 23
        minutes - integer between 0 and 59
        seconds - integer between 0 and 59

        Returns:
        time interval in seconds.
        """
        if hours == 0 and minutes == 0 and seconds == 0:
            self._sample_delay = 60  # default interval of 1 minute
        else:
            self._sample_delay = hours * 3600 + minutes * 60 + seconds

    def com_open(self, port):
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
            self.abort = True
        else:
            time.sleep(2)
            return ser



    def get_sample(self):
        ser = self.com_open(self.port) #Open a serial comm link

        #
        sample_data = {t:time.strftime('%{}'.format(t)) for t in self.timefmt}

        # set next sample time ready for next loop
        self.next_sample_time = time.time() /
                                + self.sample_delay /
                                + self.calibration

        #send a byte to weather station triggering sampling of sensors
        ser.write(self.send_byte.encode())

        # read newest data from Arduino weather station
        rcvd = str(ser.readline(), 'utf8').strip('\r\n')
        ser.close() #Close the serial com link

        rcvdata = rcvd.split(',')
        sample_data.update({rc:rcvdata[self.rcvdatafmt.index(rc)]
                    for rc in self.rcvdatafmt})

        return sample_data

    def write_file(self, data):
        #build the Filename using logtime
        filetime = '{}-{}-{}_{}-{}-{}'.format(
                                        data['Y'], data['m'], data['d'],
                                        data['H'], data['M'], data['S']
                                        )
        #build the date field
        datefield = '{}/{}/{}'.format(data['d'], data['m'], data['Y'])

        #build the ti[][me field
        timefield = '{}:{}:{}'.format(data['H'], data['M'], data['S'])

        if self.first_run:
            # create log file
            if self.default_file:
                file_path =r'{}\{}.csv'.format(self.file_dir, filetime)
            else:
                file_path = fp + '_{}.csv'.format(filetime)

            #TODO  rewrite using exception handling. is it more efficient?
            if not os.path.exists(self.file_dir):
                os.mkdir(self.file_dir)
            with open(file_path,'x') as file:
                file.write('Date,Time,Temperature \u00b0C,Pressure Pa,Humidity %\n')
            file.close()
            self.first_run = False
        #write to log file
        with open(file_path, 'a') as file:
            file.write('{},{},{},{},{}\n'.format(
                                        datefield, timefield,
                                        data['t'], data['p'], data['h']
                                        ))
            file.close()
            return
