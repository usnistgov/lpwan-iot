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
    """x"""
    ser.write(b'response to the listd command\n')


def send_copyd_output_to_fipy(ser, command):
    """x"""
    ser.write(b'response to the copyd command\n')


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
