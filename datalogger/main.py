# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties.  Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain.  NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

# Certain commercial entities, equipment, or material may be
# identified in this document in order to describe an experimental
# procedure or concept adequately. Such identification is not intended
# to imply recommendation or endorsement by NIST, nor is it intended
# to imply that the entities, materials, or equipment are necessarily
# the best available for the purpose.

"""Program, to be run on a pycom fipy, to collect data from a
dataTaker datalogger over the dataTaker's serial port.

In this configuration, the Fipy is connected both to a laptop (via
UART0) and to the dataTaker device (via UART1).

Important connectivity info:

FT232 USB-to-TTL converter board plugged into the laptop's USB: 
    the voltage level switch set to 5V VCC
    VCC connected to Red
    GND connected to Yellow
    TXD connected to Green
    RXD connected to Purple

On the Fipy:
    Red connected to + power rail on breadboard
    Yellow connected to - power rail on breadboard
    Green connected to Fipy Pin 40 (the program port's RX0)
    Purple connected to Fipy Pin 41 (the program port's TX0)

NulSom INc. Ultra Compact RS232 to TTL Converter with Male DB9:
    Connected using the DB9 connector, through a Null Modem adapter, to
        the dataTaker's serial port. The Null Modem adapter is needed.
    The TTL side of this device is connected using different wires from
        those described above (but sometimes the same colors)
    VCC connected to Red
    GND connected to Black
    RX connected to White
    Tx connected to Brown

On the Fipy:
    Red connected to + power rail on breadboard
    Black connected to - power rail on breadboard
    Brown connected to Pin 24 (the Tx of UART1)
    White connected to Pin 21 (the Rx of UART1)
"""

import sys
import machine
from machine import UART
import time
from network import LoRa
import binascii
import struct
import pycom
import socket

import mykeys

__author__ = "Sebastian Barillaro and Lee Badger"


def main():
    """Execution starts here, after all functions have been defined."""
    print('my Fipy starting up!')

    uart = get_configured_uart()
    time.sleep(1.0)

#    jobs_list = get_jobs_list_from_datataker(uart)
#    print('the returned jobs: ', jobs_list)

    records = get_records_from_datataker(uart)
    cur_record_index = 0
    max_record_index = len(records) - 1

    print('num_records', len(records))
    print('first record:', records[0])
    print('last record:', records[01])
    #print('the returned records: ', records)

    pycom.heartbeat(False)

    app_swkey = binascii.unhexlify(mykeys.app_swkey)
    nwk_swkey = binascii.unhexlify(mykeys.nwk_swkey)

    lora = LoRa(mode=LoRa.LORAWAN,
                region=LoRa.US915,
                device_class=LoRa.CLASS_C,
                tx_retries=0)
    dev_EUI = binascii.hexlify(lora.mac()).upper().decode('utf-8')

    (fipy_number, dev_addr) = get_fipy_number_and_address(dev_EUI)
    print('device fipy_number:', fipy_number)
    print('device EUI:', dev_addr)
    subband = 2
    select_subband(lora, subband)
    lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))
    print('Network joined!')

    blinkDebug(0x00FF00,0.1,5)

    sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 0)
    
    cycle = 0
    msgReceived = 0
    my_counter = 0
    while True:
        ### add your repeated execution code here

        print("Cycle: " , cycle)

        #static date-time value for now
        #dt_time_val = '2018/09/04 16:40:00.000'
        #dt_temp_val = '22.703516'

        cur_record = records[cur_record_index]
        if cur_record_index >= max_record_index:
            cur_record_index = 0
        else:
            cur_record_index += 1
        dt_time_val = cur_record[0]
        dt_temp_val = cur_record[1]
        
        date_and_hours, time_and_temp = encode_time_temp_value(dt_time_val, dt_temp_val)

        my_counter += 1
        int_counter = int(my_counter)

        payload = (struct.pack('>l', date_and_hours) + struct.pack('>l', time_and_temp))

        sock.bind(1)

        print("payload =", str(payload))

        sock.setblocking(True)
        try:
            sock.send(payload)
            print("message sent")
            blinkDebug(0x111111,0.2,len(payload))
        except OSError as e:
            if e.args[0] == 11:
                print ("error sending payload")
                blinkDebug(0x111111,2,10)

        sock.setblocking(False)

        # get any data received (if any...)
        data = sock.recv(64)
        if len(data) > 0:
            print ("received ", len(data),": ", str(data))
            print(data)
            blinkDebug(0x0000FF,1.0,len(data))
            msgReceived = msgReceived + 1
        else:
            print ("nothing received")

        delay = 10
        blinkDebug(0x0000FF,2.0,msgReceived)
        print("Delay:", delay)
        time.sleep(delay)
        cycle = cycle + 1
        print("")


def get_fipy_number_and_address(dev_EUI):
    """Return a tuple: (fipy_number,  device_address), based on its dev_EUI."""
    if (dev_EUI == "70B3D5499439D0FC"):
        print ("dev_addr: ", '2602154D')
        dev_addr = struct.unpack(">l", binascii.unhexlify('2602154D'))[0]
        return(1, dev_addr)
    if (dev_EUI == "70B3D5499FF4E468"):
        print ("dev_addr: ", '26021CC7')
        dev_addr = struct.unpack(">l", binascii.unhexlify('26021CC7'))[0]
        return(2, dev_addr)
    if (dev_EUI == "70B3D549978AF56A"):
        FiPyNumber = 3
        dev_addr = struct.unpack(">l", binascii.unhexlify('2602150A'))[0]
        return(3, dev_addr)
    if (dev_EUI == "70B3D5499C85C244"):
        dev_addr = struct.unpack(">l", binascii.unhexlify('26021A26'))[0]
        return(4, dev_addr)

    print ("Error, did not find a fipy. Blinking RED x", FiPyNumber)
    blinkDebug(0xFF0000,1,FiPyNumber)
    print("dev_EUI: " + dev_EUI)
    print("app_swkey: " + binascii.hexlify(app_swkey).upper().decode('utf-8'))
    print("nwk_swkey: " + binascii.hexlify(nwk_swkey).upper().decode('utf-8'))
    return(None)


def blinkDebug(color, tOn, tTimes):
    """Use the Fipy's LED to show error status."""
    times = 0
    while times < tTimes:
        pycom.rgbled(color)
        time.sleep(tOn)
        pycom.rgbled(0x000000)
        time.sleep(tOn * 0.50)
        times = times + 1


def select_subband(lora, subband):
    """Prevent the use of channels that are not supported by our gateway."""
    if type(subband) is int:
        if (subband<1) or (subband>8):
            raise ValueError("subband out of range (1-8)")
    else:
        raise TypeError("subband must be 1-8")

    #print("[select_subband] subband = ", subband, "Blinking blue x", subband)
    blinkDebug(0x0000FF,1,subband)

    #print("[select_subband] Removing unused channels according to subband =",
    #      subband)
    for channel in range(0, 72):
        if (((channel >= (subband-1)*8 and channel < ((subband-1)*8)+8))
                or (channel == 63+subband)):
            pass
            #print("[select_subband] NOT removing channel:", channel,
            #      "- Frequency =", (902300000+channel*200000)/1000000, "MHz")
        else:
            x = lora.remove_channel(channel)
            #print("[select_subband] removing channel:", channel,
            #      "- Frequency =", (902300000+channel*200000)/1000000, "MHz")
    #print("[select_subband] WARNING! " +
    #      "Frequency for channel >= 64 are wrong! channel",
    #      63+subband, "=", 903+(subband-1)*1.6,
    #      "MHz")


def get_jobs_list_from_datataker(uart):
    """Return a list of jobs currently configured in the datataker."""
    jobs_list = []
    s = uart.write('listd\r\n')
    time.sleep(1.0)  #NOTE! static delays may need tuning for dataTaker
    while uart.any():
        bytes_value = uart.readline()
        line = bytes_value.decode()
        if line:
            #print('line:', line)
            #First line of the listd output
            if line.strip() == 'listd':
                time.sleep(0.2)
                continue

            line_parts = line.split()

            #Second line of the listd output
            if line_parts[0] == 'Job' and line_parts[1] == 'Sch':
                time.sleep(0.2)
                continue

            #Third line of the listd output
            if line_parts[0] == '========':
                time.sleep(0.2)
                continue

            #Last line of the listd output
            if line.strip() == 'DT80>':
                time.sleep(0.2)
                continue

            job_path = line_parts[-1]
            jobs_list.append(job_path)
        else:
            print('uart.readline() failed!')
        time.sleep(0.2)
    return(jobs_list)


def encode_time_temp_value(dt_time_val, dt_temp_val):
    """Encode a dataTaker time and temp values into 2 4-byte values to send
    via LORA.

    This function assumes we have only two 4-bytes values to work
    with, so we use every byte.
    """
    #Recognize a value like: 2018/09/04 16:40:00.000

    # Encode the date part, a value like: 2018/09/04
    date_val = dt_time_val.split()[0]
    year = date_val.split('/')[0]
    month = date_val.split('/')[1]
    day = date_val.split('/')[2]

    # Given that all years of interest will be in the same millennium,
    # send only the lowest 3 digits of the 4-digit year (e.g., for
    # 2018, send 018), and add the 2000 back on the server side.
    year_int = int(year)
    year_int -= 2000
    year_bits = year_int <<24

    month_int = int(month)
    month_bits = month_int <<16

    day_int = int(day)
    day_bits = day_int <<8

    # Recognize the time part, a value like: 16:40:00.000
    time_val = dt_time_val.split()[1]
    time_val = time_val.strip()
    hours = time_val.split(':')[0]
    minutes = time_val.split(':')[1]
    seconds = time_val.split(':')[2]
    whole_seconds = seconds.split('.')[0]
    microseconds = seconds.split('.')[1]

    hours_int = int(hours)
    hours_bits = hours_int

    # Pack values into first int to return
    date_and_hours_val = year_bits | month_bits | day_bits | hours_bits

    minutes_int = int(minutes)
    minutes_bits = minutes_int <<24
    whole_seconds_int = int(whole_seconds)
    whole_seconds_bits = whole_seconds_int <<16

    # A temperature looks like:  22.703516
    degrees = dt_temp_val.split('.')[0]
    degrees_int = int(degrees)
    degrees_bits = degrees_int << 8

    fractional_degrees = dt_temp_val.split('.')[1]
    fractional_degrees = fractional_degrees[:2]
    fractional_degrees_bits = int(fractional_degrees)

    # Pack values into second int to return
    time_and_temp_val = minutes_bits | whole_seconds_bits | degrees_bits | fractional_degrees_bits

    return (date_and_hours_val, time_and_temp_val)


def get_records_from_datataker(uart):
    """Return a list of (time, temp) tuples, collected from the dataTaker."""
    records = []
    s2 = uart.write('copyd archive=y start=2018-08-29T16:00:00.000\r\n')
    time.sleep(4.0) #NOTE! may have to tune the static delay for the dataTaker
    while uart.any():
        bytes_value = uart.readline()
        line = bytes_value.decode()
        if line:
            line_parts = line.split(',')
            #print('len:', len(line_parts))
            #print('part0:', line_parts[0])

            #Filter out the header line.
            if is_time_value(line_parts[0]):
                rec = tuple([line_parts[0], line_parts[2]])
                records.append(rec)
        else:
            print('uart.readline() failed!')
        time.sleep(0.4)
    return(records)


def is_time_value(val):
    """Return True iff the string is in dataTaker date/time format."""
    #Recognize a value like: 2018/09/04 16:40:00.000
    if len(val.split()) != 2:
        return(False)

    # Recognize the date part, a value like: 2018/09/04
    date_val = val.split()[0]
    if len(date_val.split('/')) != 3:
        return(False)
    year = date_val.split('/')[0]
    month = date_val.split('/')[1]
    day = date_val.split('/')[2]
    if (not (year.isdigit()
             and month.isdigit()
             and day.isdigit())):
        return(False)

    # Recognize the time part, a value like: 16:40:00.000
    time_val = val.split()[1]
    hours = time_val.split(':')[0]
    minutes = time_val.split(':')[1]
    seconds = time_val.split(':')[2]
    whole_seconds = seconds.split('.')[0]
    microseconds = seconds.split('.')[1]
    if (not (hours.isdigit()
             and minutes.isdigit()
             and whole_seconds.isdigit()
             and microseconds.isdigit())):
        return(False)

    return(True)


def get_configured_uart():
    """Allocates and initializes a UART object, and returns it."""
    #datataker default settings
    uart = UART(1, 57600)
    uart.init(57600, bits=8, parity=None, stop=1)
    return(uart)


if __name__ == '__main__':
    main()
