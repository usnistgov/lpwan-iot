#!/usr/local/bin/python3

#IN-PROGRESS code.

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

"""This program reads several dataTaker Series 3 (see
www.datataker.com) commands from a serial port and generates synthetic
responses. The purpose of the program is interoperability testing
prior to integration with a real dataTaker.

For each line of data read from a serial port, this program checks if
the line is one of the simulated commands and, if so, writes a
response back on the same serial port. The response written is
structured to be similar to what a real dataTaker would generate, but
is entirely synthetic.
"""

#credit:
#stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package

import argparse
import time
import serial
import sys

__author__ = "Lee Badger"

def main():
    """Execution starts here, after all the functions are defined."""
    parser = argparse.ArgumentParser(description=('Simulated Logger'))
    parser.add_argument('serial_port', help='e.g., /dev/cu.usbserial-A105JITH')
    args = parser.parse_args()

    ser = get_opened_serial_port(args.serial_port)

    time.sleep(1.0)

    try:
        while True:
            command = read_a_line(ser)
            if 'listd' in command:
                send_listd_output_to_fipy(ser, command)
            elif 'copyd' in command:
                send_copyd_output_to_fipy(ser, command)
            else:
                error_msg = 'invalid command: ' + command
                send_error_message_to_fipy(ser, error_msg)
    except:
        print('simulated_datataker exiting...')


def get_opened_serial_port(file_path):
    serial_port = serial.Serial(port=file_path,
                                baudrate=9600,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS)
    return(serial_port)


def send_listd_output_to_fipy(ser, command):
    """Return representative listd data, as a real datalogger would.

    The following output data was produced by a dataTaker DT80, over
    its serial port, in response to the 'listd' command.

    The communications options for the dataTaker's serial (host) port
    were:
        command mode
        57600
        8
        1
        none
        software
    """
    captured_listd_output = """listd
 Job      Sch Type       Ov Lg Go  Recs      Capacity  First                Last                 File
 ======== === ========== == == ==  ========  ========  ===================  ===================  ===========================================
*CONFIG   A   Data  Live Y  Y  Y       2380    249660  2018-08-09 10:30:00  2018-09-04 17:20:00  B:\JOBS\CONFIG\A\DATA_A.DBD
"""
    ser.write(captured_listd_output.encode())


def send_copyd_output_to_fipy(ser, command):
    """Return representative copyd data, as a real datalogger would.

    The following data was produced by a dataTaker DT80, over its
    serial port, in response to the command:

        copyd archive=y start=2018-08-29T16:00:00.000

    This command requested all records after a point in time,
    including records that have been written to archive files.

    The command produces CSV and generate a header-row."""

    captured_copyd_output = """DT80> "Timestamp","TZ","T3 TC_1B (degC)","T3 TC_1P (degC)","T3 TC_2B (degC)","T3 TC_2P (degC)","T3 TC_3B (degC)","T3 TC_3P (degC)","T3 TC_4B (degC)","T3 TC_4P (degC)","T3 TC_5B (degC)","T3 TC_5P (mv)","T3 TC_6B (mv)","T3 TC_6P (degC)","T3 TC_7B (degC)","T3 TC_7P (degC)","T3 NR2lite VDC (mv)","T3 Pyran UP  VDC (mV)","T3 Pyran Down VDC (mV)","T3 SDI12_0 (U-velocity)","T3 SDI12_1 (V-velocity)","T3 SDI12_2 (status)"
2018/08/29 16:00:00.001,n,22.703516,OverRange,OverRange,22.456284,OverRange,OverRange,22.651436,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/08/29 16:10:00.005,n,22.956048,OverRange,OverRange,22.617792,OverRange,OverRange,22.825902,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/08/29 16:20:00.007,n,22.79914,OverRange,OverRange,22.517224,OverRange,OverRange,22.716694,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 16:20:00.005,n,22.766832,OverRange,OverRange,21.913016,OverRange,OverRange,22.520006,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 16:30:00.006,n,22.919674,OverRange,OverRange,22.113522,OverRange,OverRange,22.728958,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 16:40:00.000,n,23.503174,OverRange,OverRange,22.715282,OverRange,OverRange,23.191666,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 16:50:00.000,n,24.045942,OverRange,OverRange,22.895158,OverRange,OverRange,24.045942,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 17:00:00.000,n,23.744868,OverRange,OverRange,22.939612,OverRange,OverRange,23.377162,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 17:10:00.005,n,23.51624,OverRange,OverRange,22.51059,OverRange,OverRange,23.226038,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 17:20:00.000,n,23.415284,OverRange,OverRange,22.456824,OverRange,OverRange,23.31993,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 17:30:00.000,n,23.6982,OverRange,OverRange,22.60572,OverRange,OverRange,23.403764,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 17:40:00.000,n,23.670172,OverRange,OverRange,22.8814,OverRange,OverRange,23.553204,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 17:50:00.004,n,23.685292,OverRange,OverRange,22.926718,OverRange,OverRange,23.460002,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 18:00:00.007,n,23.736564,OverRange,OverRange,22.926016,OverRange,OverRange,23.589286,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 18:10:00.000,n,23.854036,OverRange,OverRange,23.126062,OverRange,OverRange,23.70679,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 18:20:00.000,n,23.875268,OverRange,OverRange,22.809004,OverRange,OverRange,23.719552,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 18:30:00.000,n,23.842532,OverRange,OverRange,23.05402,OverRange,OverRange,23.76477,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 18:40:00.000,n,23.656604,OverRange,OverRange,22.90214,OverRange,OverRange,23.556964,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 22:30:00.013,n,21.905168,OverRange,OverRange,21.718812,OverRange,OverRange,21.97017,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 22:40:00.000,n,22.283358,OverRange,OverRange,21.897616,OverRange,OverRange,22.339816,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 22:50:00.000,n,22.512174,OverRange,OverRange,21.952982,OverRange,OverRange,22.585782,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 23:00:00.000,n,22.63168,OverRange,OverRange,21.994402,OverRange,OverRange,22.679422,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 23:10:00.000,n,22.766266,OverRange,OverRange,22.176562,OverRange,OverRange,22.831352,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 23:20:00.000,n,22.97408,OverRange,OverRange,22.310782,OverRange,OverRange,23.013114,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
2018/09/04 23:30:00.001,n,23.142354,OverRange,OverRange,22.401118,OverRange,OverRange,23.207392,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,OverRange,NotYetSet,NotYetSet,NotYetSet
Unload complete.
"""
    ser.write(captured_copyd_output.encode())
    #ser.write(b'response to the copyd command\n')


def send_error_message_to_fipy(ser, error_msg):
    """x"""
    ser.write(error_msg.encode())


def read_a_line(ser):
    """Read a line from the passed serial port; assume '\n' termination.

    Returns a string.
    """
    line = ''
    while True:
        if ser.in_waiting:
            one_byte = ser.read(1)
            line += one_byte.decode()
            if line.endswith('\n'):
                return(line)
        else:
            time.sleep(0.1)


if __name__ == '__main__':
    main()
