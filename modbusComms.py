from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.register_read_message import ReadInputRegistersResponse
import numpy as np

'''
######################################################################################################
# convert the data from its current form (interpreted as integer) into half-precion floating point form (float16) using numpy
data = str(bin(list_of_registers[0]))
data= data[0:2] +"0" + data[2:]
print(data)

S = int(data[0])
E = int(data[3:8],2)
T = int(data[8:18],2)
print(data)
print('-----------------------------------')
print(S)
print('-----------------------------------')
print(E)
print('-----------------------------------')
print(T)
print()

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

print(value)
'''

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


######################################################################################################
#print(type(value.registers[1]))



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
    telemetries = telemetries +"Array_Vmp(V):" + str(data) +","
  
    return telemetries
    


def main():
    
    setup_connection_with_Prostar_MPPT()
    
    
    mppt_data = read_telemetries_from_Prostar_MPPT()
    print(mppt_data);





    
    
    
            

if __name__== '__main__':
    main()
      