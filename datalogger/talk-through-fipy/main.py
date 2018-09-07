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

"""Program, to be run on a pycom fipy, to collect data incrementally
from a dataTaker datalogger over the dataTaker's serial port.
"""

import sys
import machine
from machine import UART
import time

def main():
    """Execution starts here, after all functions have been defined."""
    print('From my pycom!')

    uart = get_configured_uart()

    s = uart.write('listd\r\n')
    time.sleep(0.2)
    line = uart.readline()
    if line:
        print('datalogger said: ', line.decode())
    else:
        print('readline failed!')

    s2 = uart.write('copyd\r\n')

    print('s: ' , s)
    print('s2: ' , s2)


def simulate_listd_command(logger_uart):
    """x"""
    num_sent = logger_uart.write('listd\r\n')
    

def get_configured_uart():
    """Allocates and initializes a UART object, and returns it."""
    uart = UART(1, 9600)
    uart.init(9600, bits=8, parity=None, stop=1)
    return(uart)


# #This loop echos input, as characters are typed, and then the whole line.
#while True:
#    line = input()
#    #line = sys.stdin.readline()
#    sys.stdout.write('[[' + line + ']]')

#initialize UART1 for talking with the datataker.
# (we are using UART0 for the console)


"""
ser = serial.Serial(
    port = '/dev/cu.usbserial',
    baudrate=57600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff=True
)

print ser

num = ser.write(b'dir\r\n')
print 'num is: ', num
time.sleep(1)

response = ser.read(80)
"""

if __name__ == '__main__':
    main()
