# -*- coding: utf-8 -*-
"""

Core OpenBCI object for handling connections and samples from the board.

EXAMPLE USE:

def handle_sample(sample):
    print(sample.channels)

board = OpenBciBoard()
board.printRegisterSettings()
board.start(handle_sample)

NOTE: If daisy modules is enabled, the callback will occur every two 
samples, hence packet_id will only contain even numbers. As a side 
effect, the sampling rate will be divided by 2.

FIXME: at the moment we can just force daisy mode, do not check that 
the module is detected.

"""

import serial
import struct
import numpy as np
import time
import timeit
import atexit
import logging
import threading
import sys
import pdb
import glob
import tkMessageBox

SAMPLE_RATE = 250.0 # Hz
START_BYTE = 0xA0   # start of data packet
END_BYTE = 0xC0     # end of data packet
ADS1299_Vref = 4.5  # reference voltage for ADC in ADS1299. 
                    # set by its hardware
ADS1299_gain = 24.0 # assumed gain setting for ADS1299.  
                    # set by its Arduino code

scale_fac_uVolts_per_count = ADS1299_Vref/float((pow(2,23)-1))/ADS1299_gain
scale_fac_accel_G_per_count = 0.002 /(pow(2,4)) #assume set to +/4G, so 2 mG 

"""
#Commands for in SDK http://docs.openbci.com/software/01-Open BCI_SDK:

command_stop = "s";
command_startText = "x";
command_startBinary = "b";
command_startBinary_wAux = "n";
command_startBinary_4chan = "v";
command_activateFilters = "F";
command_deactivateFilters = "g";
command_deactivate_channel = {"1", "2", "3", "4", "5", "6", "7", "8"};
command_activate_channel = {"q", "w", "e", "r", "t", "y", "u", "i"};
command_activate_leadoffP_channel = {"!", "@", "#", "$", "%", "^", "&", "*"};  //shift + 1-8
command_deactivate_leadoffP_channel = {"Q", "W", "E", "R", "T", "Y", "U", "I"};   //letters (plus shift) right below 1-8
command_activate_leadoffN_channel = {"A", "S", "D", "F", "G", "H", "J", "K"}; //letters (plus shift) below the letters below 1-8
command_deactivate_leadoffN_channel = {"Z", "X", "C", "V", "B", "N", "M", "<"};   //letters (plus shift) below the letters below the letters below 1-8
command_biasAuto = "`";
command_biasFixed = "~";
"""

class OpenBciBoard(object):
    """
    Handle a connection to an OpenBCI board.

    Args:
        port: The port to connect to.
        baud: The baud of the serial connection.
        daisy: Enable or disable daisy module and 16 chans readings
    """
    def __init__(self, 
            port=None, baud=115200, 
            filter_data=False, scaled_output=True, 
            daisy=False, log=True, timeout=None
            ):

        self.log = log # print_incoming_text needs log
        self.streaming = False
        self.baudrate = baud
        self.timeout = timeout
        if not port:
            port = self.findPort()
        self.port = port
        print("Connecting to V3 at port %s" %(port))
        self.ser = serial.Serial(port= port, baudrate = baud, timeout=timeout)

        print("Serial established...")

        time.sleep(2)
        #Initialize 32-bit board, doesn't affect 8bit board
        self.ser.write(b'v');

        #wait for device to be ready
        time.sleep(1)
        self.printIncomingText()

        self.streaming = False
        self.filtering_data = filter_data
        self.scaling_output = scaled_output
        # number of EEG channels per sample *from the board*
        self.eeg_channels_per_sample = 8 
        # number of AUX channels per sample *from the board*
        self.aux_channels_per_sample = 3 
        self.read_state = 0
        self.daisy = daisy
        self.last_odd_sample = OpenBciSample(-1, [], []) # used for daisy
        self.log_packet_count = 0
        self.attempt_reconnect = False
        self.last_reconnect = 0
        self.reconnect_freq = 5
        self.packets_dropped = 0

        #Disconnects from board when terminated
        atexit.register(self.disConnect)
  
    def getSampleRate(self):
        if self.daisy:
            return SAMPLE_RATE/2
        else:
            return SAMPLE_RATE
  
    def getNbEegChannels(self):
        if self.daisy:
            return self.eeg_channels_per_sample*2
        else:
            return self.eeg_channels_per_sample
  
    def getNbAuxChannels(self):
        return  self.aux_channels_per_sample

    def startStreaming(self, callback, lapse=-1):
        """
        Start handling streaming data from the board. Call a provided 
        callback for every single sample that is processed (every two 
        samples with daisy module).

        Args:
            callback: A callback function -- or a list of functions --
                that will receive a single argument of the
            OpenBCISample object captured.
        """
        if not self.streaming:
            self.ser.write(b'b')
            self.streaming = True

        start_time = timeit.default_timer()

        # Enclose callback funtion in a list if it comes alone
        if not isinstance(callback, list):
            callback = [callback]

        #Initialize check connection
        self.checkConnection()

        while self.streaming:
            # read current sample
            sample = self.readSerialBinary()
            # if a daisy module is attached, wait to concatenate 
            # two samples (main board + daisy) before passing it 
            # to callback
            if self.daisy:
                # odd sample: daisy sample, save for later
                if ~sample.id % 2:
                    self.last_odd_sample = sample
                # even sample: concatenate and send if last 
                # sample was the fist part, otherwise drop the 
                # packet
                elif sample.id - 1 == self.last_odd_sample.id:
                    # the aux data will be the average between 
                    # the two samples, as the channel samples 
                    # themselves have been averaged by the board
                    avg_aux_data = list((np.array(sample.aux_data)\
                            + np.array(self.last_odd_sample.aux_data))/2)
                    whole_sample = OpenBciSample(sample.id, 
                            sample.channel_data +\
                                    self.last_odd_sample.channel_data, 
                            avg_aux_data)
                    for call in callback:
                        call(whole_sample)
            else:
                for call in callback:
                    call(sample)
      
            if(lapse > 0 and timeit.default_timer() - start_time > lapse):
                self.stopStreaming();
            if self.log:
                self.log_packet_count = self.log_packet_count + 1;
  
    """
    PARSER:
    Parses incoming data packet into OpenBCISample.
    Incoming Packet Structure:
    Start Byte(1)|Sample ID(1)|Channel Data(24)|Aux Data(6)|End Byte(1)
    0xA0|0-255|8, 3-byte signed ints|3 2-byte signed ints|0xC0
    """
    def readSerialBinary(self, max_bytes_to_skip=3000):
            #scale_factor=(4.5/24/(float(pow(2,23)-1)))):
        def read(n):
            b = self.ser.read(n)
            if not b:
                self.warnLogging('Device appears to be stalled. Quitting...')
                sys.exit()
                raise Exception('Device Stalled')
                sys.exit()
                return '\xFF'
            else:
                return b

        for rep in range(max_bytes_to_skip):
            #---------Start Byte & ID---------
            if self.read_state == 0:
                b = read(1)
        
                if struct.unpack('B', b)[0] == START_BYTE:
                    if(rep != 0):
                        self.warnLogging('Skipped %d bytes before start found' %(rep))
                        rep = 0;
                    #packet id goes from 0-255
                    packet_id = struct.unpack('B', read(1))[0] 
                    log_bytes_in = str(packet_id);

                    self.read_state = 1

            #---------Channel Data---------
            elif self.read_state == 1:
                channel_data = []
                for c in range(self.eeg_channels_per_sample):
                    #3 byte ints
                    literal_read = read(3)

                    unpacked = struct.unpack('3B', literal_read)
                    log_bytes_in = log_bytes_in + '|' + str(literal_read);

                    #3byte int in 2s compliment
                    if (unpacked[0] >= 127):
                        pre_fix = bytes(bytearray.fromhex('FF')) 
                    else:
                        pre_fix = bytes(bytearray.fromhex('00'))

                    literal_read = pre_fix + literal_read;

                    # unpack little endian(>) signed integer(i) 
                    # (makes unpacking platform independent)
                    myInt = struct.unpack('>i', literal_read)[0]

                    if self.scaling_output:
                        channel_data.append(myInt*scale_fac_uVolts_per_count)
                    else:
                        channel_data.append(myInt)

                self.read_state = 2;

            #---------Accelerometer Data---------
            elif self.read_state == 2:
                aux_data = []
                for a in range(self.aux_channels_per_sample):
                    #short = h
                    acc = struct.unpack('>h', read(2))[0]
                    log_bytes_in = log_bytes_in + '|' + str(acc);

                    if self.scaling_output:
                        aux_data.append(acc*scale_fac_accel_G_per_count)
                    else:
                        aux_data.append(acc)

                self.read_state = 3;
            #---------End Byte---------
            elif self.read_state == 3:
                val = struct.unpack('B', read(1))[0]
                log_bytes_in = log_bytes_in + '|' + str(val);
                self.read_state = 0 #read next packet
                if (val == END_BYTE):
                    channel_data=np.double(np.array(channel_data))
                    #channel_data*=scale_factor
                    sample = OpenBciSample(packet_id, channel_data, aux_data)
                    self.packets_dropped = 0
                    return sample
                else:
                    self.warnLogging(
                            "ID:<%d> <Unexpected END_BYTE found <%s> instead of <%s>"
                            % (packet_id, val, END_BYTE))
                    logging.debug(log_bytes_in);
                    self.packets_dropped = self.packets_dropped + 1
  
    """
    Clean Up (atexit)
    """
    def stopStreaming(self):
        print("Stopping streaming...\nWaiting for buffer to flush...")
        self.streaming = False
        self.ser.write(b's')
        if self.log:
            logging.warning('sent <s>: stopped streaming')

    def disConnect(self):
        if self.streaming == True:
            self.stopStreaming()
            time.sleep(0.2)
        if self.ser.isOpen():
            print("Closing Serial...")
            self.ser.close()
            logging.warning('serial closed')
    
    """
    SETTINGS AND HELPERS
    """
    def warnLogging(self, text):
        if self.log:
        #log how many packets where sent succesfully in between warnings
            if self.log_packet_count:
                logging.info('Data packets received:'+str(self.log_packet_count))
                self.log_packet_count = 0;
            logging.warning(text)
        print("WARNING:program:%s" % text)

    def printIncomingText(self):
        """
        When starting the connection, print all the debug data until
        we get to a line with the end sequence '$$$'.
        """
        line = ''
        #Wait for device to send data
        time.sleep(1)
    
        if self.ser.inWaiting():
            line = ''
            c = ''
            #Look for end sequence $$$
            while '$$$' not in line:
                c = self.ser.read().decode('utf-8')
                line += c
            print(line);
        else:
            self.warnLogging("No Message")

    def openBciId(self, serial):
        """
        When automatically detecting port, parse the serial return for the 
        "OpenBCI" ID.
        """
        line = ''
        #Wait for device to send data
        time.sleep(2)
    
        if serial.inWaiting():
            line = ''
            c = ''
            #Look for end sequence $$$
            while '$$$' not in line:
                c = serial.read().decode('utf-8')
                line += c
            if "BCI" in line:
                return True
        return False

    def printRegisterSettings(self):
        self.ser.write(b'?')
        time.sleep(0.5)
        self.printIncomingText();

    #DEBBUGING: Prints individual incoming bytes
    def printBytesIn(self):
        if not self.streaming:
            self.ser.write(b'b')
            self.streaming = True
        while self.streaming:
            print(struct.unpack('B',self.ser.read())[0]);
        """
        Incoming Packet Structure:
        Start Byte(1)|Sample ID(1)|Channel Data(24)|Aux Data(6)|End Byte(1)
        0xA0|0-255|8, 3-byte signed ints|3 2-byte signed ints|0xC0
        """

    def printPacketsIn(self):
        while self.streaming:
            b = struct.unpack('B', self.ser.read())[0];
      
            if b == START_BYTE:
                self.attempt_reconnect = False
                if skipped_str:
                    logging.debug('SKIPPED\n' + skipped_str + '\nSKIPPED')
                    skipped_str = ''

                packet_str = "%03d"%(b) + '|';
                b = struct.unpack('B', self.ser.read())[0];
                packet_str = packet_str + "%03d"%(b) + '|';
        
                #data channels
                for i in range(24-1):
                    b = struct.unpack('B', self.ser.read())[0];
                    packet_str = packet_str + '.' + "%03d"%(b);

                b = struct.unpack('B', self.ser.read())[0];
                packet_str = packet_str + '.' + "%03d"%(b) + '|';

                #aux channels
                for i in range(6-1):
                    b = struct.unpack('B', self.ser.read())[0];
                    packet_str = packet_str + '.' + "%03d"%(b);
        
                b = struct.unpack('B', self.ser.read())[0];
                packet_str = packet_str + '.' + "%03d"%(b) + '|';

                #end byte
                b = struct.unpack('B', self.ser.read())[0];
        
                #Valid Packet
                if b == END_BYTE:
                    packet_str = packet_str + '.' + "%03d"%(b) + '|VAL';
                    print(packet_str)
                    #logging.debug(packet_str)
        
                #Invalid Packet
                else:
                    packet_str = packet_str + '.' + "%03d"%(b) + '|INV';
                    #Reset
                    self.attempt_reconnect = True
            else:
                print(b)
                if b == END_BYTE:
                    skipped_str = skipped_str + '|END|'
                else:
                    skipped_str = skipped_str + "%03d"%(b) + '.'

            if self.attempt_reconnect and \
                    (timeit.default_timer()-self.last_reconnect) > \
                    self.reconnect_freq:
                self.last_reconnect = timeit.default_timer()
                self.warnLogging('Reconnecting')
                self.reConnect()
 
    def checkConnection(self, interval = 2, max_packets_to_skip=10):
        # check number of dropped packages and 
        # establish connection problem if too large
        if self.packets_dropped > max_packets_to_skip:
            #if error, attempt to reconect
            self.reConnect()
        # check again again in 2 seconds
        threading.Timer(interval, self.checkConnection).start()

    def reConnect(self):
        self.packets_dropped = 0
        self.warnLogging('Reconnecting')
        self.stopStreaming()
        time.sleep(0.5)
        self.ser.write(b'v')
        time.sleep(0.5)
        self.ser.write(b'b')
        time.sleep(0.5)
        self.streaming = True
        #self.attempt_reconnect = False

    #Adds a filter at 60hz to cancel out ambient electrical noise
    def enableFilters(self):
        self.ser.write(b'f')
        self.filtering_data = True;

    def disableFilters(self):
        self.ser.write(b'g')
        self.filtering_data = False;

    def testSignal(self, signal):
        if signal == 0:
            self.ser.write(b'0')
            self.warnLogging("Connecting all pins to ground")
        elif signal == 1:
            self.ser.write(b'p')
            self.warnLogging("Connecting all pins to Vcc")
        elif signal == 2:
            self.ser.write(b'-')
            self.warnLogging("Connecting pins to low frequency 1x amp signal")
        elif signal == 3:
            self.ser.write(b'=')
            self.warnLogging("Connecting pins to high frequency 1x amp signal")
        elif signal == 4:
            self.ser.write(b'[')
            self.warnLogging("Connecting pins to low frequency 2x amp signal")
        elif signal == 5:
            self.ser.write(b']')
            self.warnLogging("Connecting pins to high frequency 2x amp signal")
        else:
            self.warnLogging(
                    "%s is not a known test signal." %(signal) + \
                            "Valid signals go from 0-5" )

    def setChannel(self, channel, toggle_position):
        #Commands to set toggle to on position
        if toggle_position == 1:
            if channel is 1:
                self.ser.write(b'!')
            if channel is 2:
                self.ser.write(b'@')
            if channel is 3:
                self.ser.write(b'#')
            if channel is 4:
                self.ser.write(b'$')
            if channel is 5:
                self.ser.write(b'%')
            if channel is 6:
                self.ser.write(b'^')
            if channel is 7:
                self.ser.write(b'&')
            if channel is 8:
                self.ser.write(b'*')
            if channel is 9 and self.daisy:
                self.ser.write(b'Q')
            if channel is 10 and self.daisy:
                self.ser.write(b'W')
            if channel is 11 and self.daisy:
                self.ser.write(b'E')
            if channel is 12 and self.daisy:
                self.ser.write(b'R')
            if channel is 13 and self.daisy:
                self.ser.write(b'T')
            if channel is 14 and self.daisy:
                self.ser.write(b'Y')
            if channel is 15 and self.daisy:
                self.ser.write(b'U')
            if channel is 16 and self.daisy:
                self.ser.write(b'I')
        #Commands to set toggle to off position
        elif toggle_position == 0:
            if channel is 1:
                self.ser.write(b'1')
            if channel is 2:
                self.ser.write(b'2')
            if channel is 3:
                self.ser.write(b'3')
            if channel is 4:
                self.ser.write(b'4')
            if channel is 5:
                self.ser.write(b'5')
            if channel is 6:
                self.ser.write(b'6')
            if channel is 7:
                self.ser.write(b'7')
            if channel is 8:
                self.ser.write(b'8')
            if channel is 9 and self.daisy:
                self.ser.write(b'q')
            if channel is 10 and self.daisy:
                self.ser.write(b'w')
            if channel is 11 and self.daisy:
                self.ser.write(b'e')
            if channel is 12 and self.daisy:
                self.ser.write(b'r')
            if channel is 13 and self.daisy:
                self.ser.write(b't')
            if channel is 14 and self.daisy:
                self.ser.write(b'y')
            if channel is 15 and self.daisy:
                self.ser.write(b'u')
            if channel is 16 and self.daisy:
                self.ser.write(b'i')

    def findPort(self):
        # Finds the serial port names
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i+1) for i in range(256)]
        elif sys.platform.startswith('linux') or \
                sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/cu.Feasycom-SPPDev*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/*ttyusb*')
        else:
            raise EnvironmentError(
                    'Error finding ports on your operating system'
                    )
        openbci_port = ''
        for port in ports:
            try:
                s = serial.Serial(port=port, 
                        baudrate=self.baudrate, 
                        timeout=self.timeout)
            except (OSError, serial.SerialException):
                continue

            try:
                s.write(b'v')
                openbci_serial = self.openBciId(s)
                s.close()
                if openbci_serial:
                    openbci_port = port;
            except:
                s.write(b's')
                logging.warning("Try to stop pre-existing streaming")
                time.sleep(0.25)
                s.close()
                time.sleep(0.25)
                s.open()
                logging.warning("Reconnect Port")
                s.write(b'v')
                openbci_serial = self.openBciId(s)
                s.close()
                if openbci_serial:
                    openbci_port = port;
                    break

        if openbci_port == '':
            tkMessageBox.showerror("错误", "找不到设备，请查看是否正确连接！")
            raise OSError('Cannot find OpenBCI port')
        else:
            return openbci_port

class OpenBciSample(object):
    """
    Object encapulsating a single sample from the OpenBCI board.
    """
    def __init__(self, packet_id, channel_data, aux_data):
        self.id = packet_id;
        self.channel_data = channel_data;
        self.aux_data = aux_data;

class ReadThread(threading.Thread):
    def __init__(self):
        super(ReadThread, self).__init__()
        # Initialize Board
        self.board=OpenBciBoard()
        print("Initialized Board")
        self.nb_of_channels=8

        # Streaming
        self.board.streaming=True

        # Initialize Raw Data
        self.raw_counts=0
        self.raw_array=None
        self.raw_size=5000
        
        # Initialize Ready Flag
        self.is_ready=False

        # Initialize Record
        self.is_record=False
        self.is_save=False
        self.rcd_counts=0
        self.rcd_array=None

        # Initialize Sliding Window
        self.nb_of_win=2500
        self.win_array=None
        self.is_running=True

        # Initialize Lock
        self.running_lock=threading.Lock()

    def run(self):
        self.board.ser.write(b'b')
        
        print("Initializing channels, waiting for 10s...")
        sample_size=1650
        while True:
            # Acquire Lock
            self.running_lock.acquire()

            # Break
            if not self.is_running: break
            
            # Read
            bin_stream=self.board.ser.read(size=sample_size)

            # Release Lock
            self.running_lock.release()
            
            # Estimation
            bin_stream=bin_stream[1:-1]
            bin_array=bin_stream.split(
                    struct.pack('B', 0xC0)+struct.pack('B', 0xA0)
                    )
            int_array=np.array([ReadChannel(ba, 8) for ba in bin_array])
            channel_data=int_array.transpose()*scale_fac_uVolts_per_count

            if self.raw_counts==0:
                self.raw_array=channel_data
            else:
                self.raw_array=np.concatenate(
                        (self.raw_array, channel_data),
                        axis=1)
            self.raw_counts+=sample_size/33
            
            # Dirty Code
            if self.raw_counts>self.raw_size:
                self.raw_array=self.raw_array[:, -self.raw_size:]
                self.raw_counts=self.raw_size

            nb_of_cur_raw=self.raw_array.shape[1]
            if not self.is_ready and nb_of_cur_raw>=self.nb_of_win:
                self.is_ready=True
                print("Ready Go!")

            if self.is_record:
                # Update Record Data
                if self.is_save:
                    if self.rcd_counts==0:
                        self.rcd_array=self.raw_array[:, -self.nb_of_win-1:-1]
                        self.rcd_array=np.concatenate(
                                (self.rcd_array, channel_data),
                                axis=1)
                    else:
                        self.rcd_array=np.concatenate(
                                (self.rcd_array, channel_data), 
                                axis=1)
                    self.rcd_counts+=sample_size/33
                    print_flag=self.rcd_counts%250
                    if print_flag==0:
                        print("Recorded %d samples" % self.rcd_counts)

                # Update Sliding Window
                if nb_of_cur_raw<self.nb_of_win:
                    self.win_array=self.raw_array
                else:
                    self.win_array=\
                            self.raw_array[:, -self.nb_of_win:]


    def stop(self):
        self.running_lock.acquire()
        self.is_running=False
        self.is_record=False
        self.is_save=False
        self.rcd_counts=0
        self.raw_counts=0
        self.board.disConnect()
        self.running_lock.release()
        self.join()

    def getWinArray(self):
        return self.win_array.copy()

    def getRawArray(self):
        return self.raw_array.copy()

    def getRcdArray(self):
        return self.rcd_array.copy()

def ReadChannel(bin_data, nb_of_channels):
    bin_channel=bin_data[1:1+3*nb_of_channels]
    try:
        unpack_data=struct.unpack('%dB' % 3*nb_of_channels, 
                bin_channel)
    except:
        return [0 for i in range(nb_of_channels)]

    all_full=[]
    for ind in range(0, 3*nb_of_channels, 3):
        if unpack_data[ind]>=127:
            pre_fix = bytes(bytearray.fromhex('FF')) 
        else:
            pre_fix = bytes(bytearray.fromhex('00')) 

        bin_full=pre_fix+bin_channel[ind:ind+3]
        int_full=struct.unpack('>i', bin_full)[0]
        all_full.append(int_full)

    return all_full

if __name__=='__main__':
    board=OpenBciBoard()
    print("Initialized Port")
    board.ser.write(b'b')
    while True:
        bin_stream=board.ser.read(size=825)
        bin_stream=bin_stream[1:-1]
        bin_array=bin_stream.split(
                struct.pack('B', 0xC0)+struct.pack('B', 0xA0)
                )
        int_array=np.array([ReadChannel(ba, 8) for ba in bin_array])
        print("data_x = %d, data_y = %d" % (int_array.shape[0], int_array.shape[1]))

#START_BYTE = 0xA0   # start of data packet
#END_BYTE = 0xC0     # end of data packet
