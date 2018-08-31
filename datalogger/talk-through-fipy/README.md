# Talk-through-fipy (PRELIMINARY)

Talk-through-fipy is an experiment to verify that we can program the
fipy to communicate both with the datalogger and a laptop at the same
time.

See the accompanying figure, talk-through-fipy-arch.jpeg.

First, the pymakr plugin must be installed in the atom editor, as
documented at: https://docs.pycom.io/pymakr/installation/atom. This
provides access, over a serial port, to the fipy's REPL
(read/evaluate/print/loop) for interactively typing commands to the
fipy and reading their outputs.

Our program, which we will upload into the fipy, will be a relay
between the the atom editor's REPL console running on the laptop, and
the datalogger.

The program running on the fipy will read each line that the user
types to the REPL console, send it to the datalogger, read the
datalogger's response, and display that response to the user.

Control-C suspends the running program on a fipy.
