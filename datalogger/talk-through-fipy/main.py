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

__author__ = "Lee Badger"

def main():
    """Execution starts here, after all functions have been defined."""
    print('From my pycom!')

    uart = get_configured_uart()
    time.sleep(1.0)

    jobs_list = get_jobs_list_from_datataker(uart)
    print('the returned jobs: ', jobs_list)

    records = get_records_from_datataker(uart)
    print('the returned records: ', records)


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
