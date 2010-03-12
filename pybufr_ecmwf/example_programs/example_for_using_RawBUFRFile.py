#!/usr/bin/env python

# This is a small example program intended to demonstrate
# how the RawBUFRFile class defined in the pybufr_ecmwf.py
# module may be used.

# For details on the revision history, refer to the log-notes in
# the mercurial revisioning system hosted at google code.
#
# Written by: J. de Kloe, KNMI, Initial version 21-Jan-2010    
#
# License: GPL v2.

import os          # operating system functions
import sys         # system functions

# import the python file defining the RawBUFRFile class
if os.path.isdir("../pybufr_ecmwf"):
    sys.path.append("../")
else:
    sys.path.append("../../")

from pybufr_ecmwf import RawBUFRFile

print "-"*50
print "reading example"
print "-"*50

# NOTE: this testfile: Testfile3CorruptedMsgs.BUFR
# hold 3 copies of Testfile.BUFR catted together, and
# was especially modified using hexedit to have
# false end markers (7777) halfway the 2nd and 3rd
# message. These messages are therefore corrupted and
# decoding them will probably result in garbage, but they
# are very usefull to test the RawBUFRFile.split() method.

# define the input test filename
if os.path.exists('testdata'):
    input_test_bufr_file = 'testdata/Testfile3CorruptedMsgs.BUFR'
else:
    input_test_bufr_file = '../testdata/Testfile3CorruptedMsgs.BUFR'

# get an instance of the RawBUFRFile class
BF = RawBUFRFile()

# open the test file for reading, count nr of BUFR messages in it
# and store its content in memory, together with
# an array of pointers to the start and end of each BUFR message
BF.open(input_test_bufr_file,'r')

# print the internal data of the class instance
BF.print_properties(prefix="RawBUFRFile (opened for reading)")

# print the number of BUFR messages in the file
n=BF.get_num_bufr_msgs()
print "This file contains: ",n," BUFR messages."

# sequentially read the raw (undecoded) BUFR messages from the class instance
data1=BF.get_next_raw_bufr_msg() # should return proper data
data2=BF.get_next_raw_bufr_msg() # should return corrupted data
data3=BF.get_next_raw_bufr_msg() # should return corrupted data
print "a warning is expected here:"
data4=BF.get_next_raw_bufr_msg() # returns with None

for i in range(1,n+1):
    # read a selected raw BUFR message from the class instance
    raw_data=BF.get_raw_bufr_msg(i)
    print "msg ",i," got ",len(raw_data)," words"

# close the file
BF.close()

# delete the class instance
del(BF)

print "-"*50
print "writing example"
print "-"*50

# define the output test filename
output_test_bufr_file = 'Testfile3Msgs.BUFR'

# make sure no file with this name exists
if (os.path.exists(output_test_bufr_file)):
    os.remove(output_test_bufr_file)

# get an instance of the RawBUFRFile class
BF1 = RawBUFRFile()

# open the test file for writing
BF1.open(output_test_bufr_file,'w')

# write a few raw (encoded) BUFR messages
BF1.write_raw_bufr_msg(data1)
BF1.write_raw_bufr_msg(data2)

# print the internal data of the class instance
BF1.print_properties(prefix="RawBUFRFile (opened for writing)")

# close the file
BF1.close()

# delete the class instance
del(BF1)

# get another instance of the RawBUFRFile class
BF2 = RawBUFRFile()

# open the test file for appending
BF2.open(output_test_bufr_file,'a')

# write a third raw (encoded) BUFR messages
BF2.write_raw_bufr_msg(data3)    

# print the internal data of the class instance
BF2.print_properties(prefix="RawBUFRFile2 (opened for appending)")

# close the file
BF2.close()

# delete the class instance
del(BF2)

print "-"*50
print "done"
print "-"*50