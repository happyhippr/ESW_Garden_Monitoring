import serial
import time
import os
import datetime
import logging
import argparse
import traceback

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse
import numpy as np

debug_mode = True


'''
function definitions
'''
def setup_logger():
    try:
        filepath_log = '/home/pi/Desktop/ESW_Garden_Monitoring/Logs/'
        #date = str(datetime.date.today())
        date = get_date()
        filepath = filepath_log+date+'/'
        print(filepath)
        if not os.path.exists(filepath):
            os.makedirs(filepath)
            global filepath_info
            filename_info = filepath + 'info.log'
            info_file = open(filename_info,'w')
            #info_file.write('utc_time,utc_zone_offset,utc_isdst,localdate,localtime,system_state,panel_voltage_(V),panel_current_(mA),panel_power(W),PWM_frequency,PWM_duty_cycle,dcdc_efficiency,load_voltage,load_current,load_power\n')

        global my_logger
        global cur_date
        my_logger = logging.getLogger('myLogger')
        my_logger.setLevel(level=logging.DEBUG)
        
        filepath_info = filepath + 'info.log'
        my_file_handler_data = logging.FileHandler(filepath_info)
        my_file_handler_data.setLevel(logging.INFO)
        formatter_info = logging.Formatter('%(message)s')
        my_file_handler_data.setFormatter(formatter_info)
        my_logger.addHandler(my_file_handler_data)
        cur_date = get_date();
        return my_logger
    
    except Exception as e:
        print(e)

def setup_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug",help ="activate debug logging",action="store_true")
    parser.add_argument("--display",help="create a display to monitor the days V,I,& P", action="store_true")
    global args
    args = parser.parse_args()

def test_logger():
    print('starting test_logger function')
    t = datetime.datetime.now().time()
    my_logger.debug('starting test_logger {}'.format(datetime.datetime.now().time()))
    my_logger.info('puttn that info downn tha hatch{}'.format(datetime.datetime.now().time()))
    my_logger.debug('finished info{}'.format(datetime.datetime.now().time()))
    print('finishing test_logger function')


def setup_serial_to_arduino():
    global serial_arduino_bus
    serial_arduino_bus = serial.Serial('/dev/ttyACM0',baudrate=9600,timeout=2)
    time.sleep(2)
    return serial_arduino_bus
    


def log_new_measurement():
    my_logger.debug('requesting data from arduino')
    d = get_date()
    if d!=cur_date:
        # create a new log file for the new day;
        setup_logger()

    t = get_time()
    utc_t = get_utctime()
    utc_tzo = get_timezone_offset()
    is_dst = get_isdst()
    #log_string = utc_t + "," + utc_tzo + "," + is_dst + "," + d + "," + t
    log_string = "utc:" +utc_t + "," + "localdate:"+d + "," +"localtime:"+ t
    
    serial_arduino_bus.write(b'2')
    data_string = str(serial_arduino_bus.readline())
    data_string = data_string[2:-5]#remove the new-line character and the binary indiactor character
    
    log_string = log_string + "," + data_string
    #print(log_string)
    #my_logger.info(log_string)
    my_logger.debug('exiting arduino_get_reading')
    
    return log_string


def setup_matplotlib_display():
    style.use('fivethirtyeight')
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)


def matplotlib_animate():
    graph_data = open(filepath_info,'r').read()
    lines = graph_data.split('\n')
    
    
def get_time():
    dt = datetime.datetime.today()
    h = str(dt.hour)
    if len(h)<2:
        h = "0" + h
    m = str(dt.minute)
    if len(m)<2:
        m = "0" + m
    s = str(dt.second)
    if len(s) < 2:
        s = "0" + s
    t = h+m+s
    return t


def get_date():
    dt = datetime.datetime.today()
    y = str(dt.year)
    m = str(dt.month)
    if len(m)<2:
        m = "0" + m
    d = str(dt.day)
    if len(d)<2:
        d = "0" + d
    date = y+m+d
    return date

def get_utctime():
    now = datetime.datetime.utcnow()
    utc_now,utc_millis = str((now-datetime.datetime(1970,1,1)).total_seconds()).split('.')
    return utc_now

def get_timezone_offset():
    return "-05:00"

def get_isdst():
    return "true"

def set_arduino_state_to_active():
    serial_arduino_bus.write(b'a')

def set_arduino_state_to_standby():
    serial_arduino_bus.write(b's')

def set_arduino_state_to_offline():
    serial_arduino_bus.write(b'a')
    
def animate(i):
    #get filepath and open file to read lines of data to plot
    date = get_date()
    filepath ="../Logs/" + date +"/info.log"
    graph_data = open(filepath,'r').read()
    lines = graph_data.split('\n')
    lt = []
    V = []
    I = []
    P = []
    
    for line in lines:
        if (len(line)>1 and len(line)<80):# ignore empty lines
            utctime,utc_tzo,is_dst,localdate,localtime,system_state,panel_voltage,panel_current,panel_power,pwm_frequency,pwm_duty_cycle,dcdc_efficiency,load_voltage,load_current,load_power = line.split(',')
            #utc_time,utc_zone_offset,utc_isdst,localdate,localtime,system_state,panel_voltage_(V),panel_current_(mA),panel_power(W),PWM_frequency,PWM_duty_cycle,dcdc_efficiency,load_voltage,load_current,load_power

            lt.append(float(localtime))
            V.append(float(bus_voltage))
            I.append(float(bus_current))
            P.append(float(bus_power))
            
    subplot_1.clear()
    subplot_2.clear()
    subplot_3.clear()
    
    subplot_1.plot(lt,V)
    subplot_2.plot(lt,I)
    subplot_3.plot(lt,P)

def setup_display():
    style.use('fivethirtyeight')

    fig = plt.figure()
    global subplot_1
    subplot_1 = plt.subplot2grid((11,1),(0,1),rowspan=2,colspan=1)
    plt.title("Voltage vs Time")
    plt.ylabel("voltage")
    plt.xlabel("localtime")
    global subplot_2
    subplot_2 = plt.subplot2grid((11,1),(3,1),rowspan=2,colspan=1)
    plt.title("Current vs Time")
    plt.ylabel("current")
    plt.xlabel("localtime")
    global subplot_3
    subplot_3 = plt.subplot2grid((11,1),(6,1),rowspan=4,colspan=1)
    plt.title("Power vs Time")
    plt.ylabel("power")
    plt.xlabel("localtime")
    
    ani = animation.FuncAnimation(fig,animate,interval=5000)
    plt.show()
    return
    
    


'''
#Create a logging object instance
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG) #set the level of things it will pay attention to
formatter_data = logging.Formatter('%(asctime)s,%(message)s')# create a instance of a format to apply to a logging object

#generate file & filepath based upon current date/time
date = str(datetime.date.today());# creating strings for filepath
date_and_time = str(datetime.datetime.now())
t = str(datetime.datetime.now().time())
directory="/home/pi/Desktop/SolarStuff/SolarPanelProject/Logs/" + date + '/'
filename= t + " info.log" 
filepath = directory+filename
print(filepath)



#create a stream handler instance to print everything to the console
stream_handler = logging.StreamHandler()
#leave stream handlers format to be default type

#create a filehandler to log signals/data recieved from the arduino to a .log file
datafile_handler = logging.FileHandler(filepath+filename);
datafile_handler.setLevel(logging.INFO)#assign its level to be info
datafile_handler.setFormatter(formatter_data)#set its format to the one assigned above

#add the created handlers to the logger to do begin their associated tasks
logger.addHandler(datafile_handler)
logger.addHandler(stream_handler)


'''
#Main Loop/funciton
'''
# main loop setup?
numRowsToCollect = 10

# setup serial connection to arduino
ser = serial.Serial('/dev/ttyACM0',baudrate=115200,timeout=2)
time.sleep(3)

#wait for input to start the data logging
userInput = input('respond with the character "y" to start loging data')

#Set the system to active mode
ser.write('a');
        
#read signal names and save to csv file
ser.write('n')
returnedData = ser.readline();
logger.info(returnedData);
print(returnedData)

# read defined number of rows of data to collect
for row in range(0,numRowsToCollect):
    ser.write('v')
    signals = ser.readline()
    logger.info(returnedData)
    print(returnedData)    
    
infoFile.close()
ser.write('o')
'''



### Used for data extracted from MPPT
def convert_int_to_float16(data):
    data = str(bin(data))
    if(len(data)<18):
        data= data[0:2] +"0" + data[2:]
        
    #print(data)

    S = int(data[0])
    E = int(data[3:8],2)
    T = int(data[8:18],2)
    '''
    print(data)
    print('-----------------------------------')
    print(S)
    print('-----------------------------------')
    print(E)
    print('-----------------------------------')
    print(T)
    print()
    '''

    value = 'nothing'
    if(E==31):
        if(T==0):
            value = 'infinity'
        if not(T==0):
            print('dengy')
            
    if(0<E<31):
        value = ((-1)**S) * (2**(E-15)) * (1+2**(-10)*T)
        
    if(E==0):
        if(T==0):
            value = 0
        if not (T==0):
            value = ((-1)**S) * (2**(-14)) * (0+(2**(-10)*T))

    return value




def setup_connection_with_Prostar_MPPT():
    ######################################################################################################
    # create a client instance that will requrest information form a server instance.
    method = 'rtu'
    port = '/dev/ttyUSB0'
    stopbits = 2
    bytesize = 8
    parity = 'N'
    baudrate = 9600
    timeout = 0.3
    global client
    client = ModbusClient(method=method,port=port,stopbits=stopbits,bytesize=bytesize,parity = parity,baudrate=baudrate,timeout=timeout)
    connection = client.connect()
    if not connection:# print true or false depending on whether a connection was established between client and server.
        print('connection failed')

def get_float16_data(register_address):
    count = 1          # How many registers should be read?
    unit = 1             # the slave unit this request is targeting
    data = client.read_input_registers(register_address,count,unit=unit).registers[0]; #get 
    data = convert_int_to_float16(data)
    return data


def read_telemetries_from_Prostar_MPPT():
    ######################################################################################################
    # Read/request register data from the server for different parameters/telemetries
    telemetries = ""
    
    #read battery terminal voltage
    register_address = 24# The address to read/request data from (aka which telemetry would you like data for? voltage? current?)
    data = get_float16_data(register_address)
    telemetries = telemetries +"Battery_Voltage(V):" + str(data) +","
    
    #read battery current
    register_address = 26# The address to read/request data from (aka which telemetry would you like data for? voltage? current?)
    data = get_float16_data(register_address)
    telemetries = telemetries +"Battery_Current(A):" + str(data) +","
    
    #read panel array voltage
    register_address = 20# The address to read/request data from (aka which telemetry would you like data for? voltage? current?)
    data = get_float16_data(register_address)
    telemetries = telemetries +"Panel_Array_Voltage(V):" + str(data) +","
    
    # Read panel array current
    register_address = 18# The address to read/request data from (aka which telemetry would you like data for? voltage? current?)
    data = get_float16_data(register_address)
    telemetries = telemetries +"Panel_Array_Current(A):" + str(data) +","
    
    
    #read Heatsink temp
    register_address = 27# The address to read/request data from (aka which telemetry would you like data for? voltage? current?)
    data = get_float16_data(register_address)
    telemetries = telemetries +"HeatSink_Temp(C):" + str(data) +","
    
    #Prostar Output power
    register_address = 61# The address to read/request data from (aka which telemetry would you like data for? voltage? current?)
    data = get_float16_data(register_address)
    telemetries = telemetries +"Prostar_Output_Power(W):" + str(data) +","
    
    # Array Voc (foudn during sweep)
    egister_address = 64# The address to read/request data from (aka which telemetry would you like data for? voltage? current?)
    data = get_float16_data(register_address)
    telemetries = telemetries +"Array_Voc(V):" + str(data) +","
    
    # Array Vmp
    egister_address = 62# The address to read/request data from (aka which telemetry would you like data for? voltage? current?)
    data = get_float16_data(register_address)
    telemetries = telemetries +"Array_Vmp(V):" + str(data)
  
    return telemetries
    




def main():    
   
    ####### Setup ##########
    print("**************Setting up Logger Instance*****************")
    setup_logger()
    print("************ Setting up Serial Communication with the Arduino *************")
    setup_serial_to_arduino()
    set_arduino_state_to_active()            
    print("************ Setting up Serial Communication with the MPPT *************")
    setup_connection_with_Prostar_MPPT()
    
    


    ####### Start LOGGING #########
    while True:
        #for i in range(1,10):
        arduino_data = log_new_measurement()
        mppt_data = read_telemetries_from_Prostar_MPPT()
        all_telemetries = arduino_data + "," + mppt_data
        print(all_telemetries);
        my_logger.info(all_telemetries)
        time.sleep(5)

    
    set_arduino_state_to_offline()
    print('completed main loop')
    
    
            

if __name__== '__main__':
    main()
            
