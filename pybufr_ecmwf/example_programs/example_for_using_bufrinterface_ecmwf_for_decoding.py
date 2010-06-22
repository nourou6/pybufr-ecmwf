#!/usr/bin/env python

"""
This is a small example program intended to demonstrate
how the pybufr_ecmwf wrapper interface to the ECMWF BUFR library may be
used for decoding a BUFR message.
"""

# For details on the revision history, refer to the log-notes in
# the mercurial revisioning system hosted at google code.
# Written by: J. de Kloe, KNMI, Initial version 25-Feb-2010    
#
# License: GPL v2.

#  #[ imported modules
import os          # operating system functions
import sys         # system functions
import numpy as np # import numerical capabilities

# set the python path to find the (maybe not yet installed) module files
# (not needed if the module is installed in the default location)
import helpers 
helpers.set_python_path()

# import the BUFR wrapper module
import pybufr_ecmwf
#  #]

# decoding_excample
def decoding_example():
    """
    wrap the example in a function to circumvent the pylint
    convention of requiring capitals for constants in the global
    scope (since most of these variables are not constants at all))
    """

    # read the binary data using the BUFRFile class
    testdata_dir = helpers.get_testdata_dir()
    input_test_bufr_file = os.path.join(testdata_dir,'Testfile.BUFR')

    print 'loading testfile: ',input_test_bufr_file
    rbf = pybufr_ecmwf.RawBUFRFile()
    rbf.open(input_test_bufr_file, 'r')
    words = rbf.get_next_raw_bufr_msg()
    rbf.close()
    
    # define the needed constants
    max_nr_descriptors          =     20 # 300
    max_nr_expanded_descriptors =    140 # 160000
    max_nr_subsets              =    361 # 25
    
    ktdlen = max_nr_descriptors
    # krdlen = max_nr_delayed_replication_factors
    kelem  = max_nr_expanded_descriptors
    kvals  = max_nr_expanded_descriptors*max_nr_subsets
    # jbufl  = max_bufr_msg_size
    # jsup   = length_ksup
    
    print '------------------------------'
    BI = pybufr_ecmwf.BUFRInterfaceECMWF()

    print "calling: decode_sections_012():"
    BI.decode_sections_012(words)

    print "calling: setup_tables()"
    BI.setup_tables()

    print "calling: print_sections_012():"
    BI.print_sections_012()
    
    # implemented upto this point
    sys.exit(0)

    # these 4 are filled by the BUS012 call above
    # ksup   = np.zeros(         9, dtype = np.int)
    # ksec0  = np.zeros(         3, dtype = np.int)
    # ksec1  = np.zeros(        40, dtype = np.int)
    # ksec2  = np.zeros(      4096, dtype = np.int)
    
    print '------------------------------'
    ksec3  = np.zeros(          4, dtype = np.int)
    ksec4  = np.zeros(          2, dtype = np.int)
    cnames = np.zeros((kelem, 64), dtype = np.character)
    cunits = np.zeros((kelem, 24), dtype = np.character)
    values = np.zeros(      kvals, dtype = np.float64) # this is the default
    cvals  = np.zeros((kvals, 80), dtype = np.character)
    kerr   = 0
    
    print "calling: ecmwfbufr.bufrex():"
    ecmwfbufr.bufrex(words, ksup, ksec0, ksec1, ksec2, ksec3, ksec4,
                     cnames, cunits, values, cvals, kerr)
    if (kerr != 0):
        print "kerr = ", kerr
        sys.exit(1)
        
    # print a selection of the decoded numbers
    print '------------------------------'
    print "Decoded BUFR message:"
    print "ksup : ", ksup
    print "sec0 : ", ksec0
    print "sec1 : ", ksec1
    print "sec2 : ", ksec2
    print "sec3 : ", ksec3
    print "sec4 : ", ksec4
    print "cnames [cunits] : "
    for (i, cnm) in enumerate(cnames):
        cun = cunits[i]
        txtn = ''.join(c for c in cnm)
        txtu = ''.join(c for c in cun)
        if (txtn.strip() != ''):
            print '[%3.3i]:%s [%s]' % (i, txtn, txtu)

    print "values : ", values
    txt = ''.join(str(v)+';' for v in values[:20] if v>0.)
    print "values[:20] : ", txt
    
    nsubsets  = ksec3[2] # 361 # number of subsets in this BUFR message

    #not yet used:
    #nelements = ksup[4] # 44 # size of one expanded subset
    
    lat = np.zeros(nsubsets)
    lon = np.zeros(nsubsets)
    for subs in range(nsubsets):
        # index_lat = nelements*(s-1)+24
        # index_lon = nelements*(s-1)+25
        index_lat = max_nr_expanded_descriptors*(subs-1)+24
        index_lon = max_nr_expanded_descriptors*(subs-1)+25
        lat[subs] = values[index_lat]
        lon[subs] = values[index_lon]
        if (30*(subs/30) == subs):
            print "subs = ", subs, "lat = ", lat[subs], " lon = ", lon[subs]
            print "min/max lat", min(lat), max(lat)
            print "min/max lon", min(lon), max(lon)
            
    print '------------------------------'
    # busel: fill the descriptor list arrays (only needed for printing)   
    
    # warning: this routine has no inputs, and acts on data stored
    #          during previous library calls
    # Therefore it only produces correct results when either bus0123
    # or bufrex have been called previously on the same bufr message.....
    # However, it is not clear to me why it seems to correctly produce
    # the descriptor lists (both bare and expanded), but yet it does
    # not seem to fill the ktdlen and ktdexl values.
    
    ktdlen = 0
    ktdlst = np.zeros(max_nr_descriptors, dtype = np.int)
    ktdexl = 0
    ktdexp = np.zeros(max_nr_expanded_descriptors, dtype = np.int)
    kerr   = 0
    
    print "calling: ecmwfbufr.busel():"
    ecmwfbufr.busel(ktdlen, # actual number of data descriptors
                    ktdlst, # list of data descriptors
                    ktdexl, # actual number of expanded data descriptors
                    ktdexp, # list of expanded data descriptors
                    kerr)   # error  message
    if (kerr != 0):
        print "kerr = ", kerr
        sys.exit(1)

    print 'busel result:'
    print "ktdlen = ", ktdlen
    print "ktdexl = ", ktdexl
    
    selection1 = np.where(ktdlst > 0)
    ktdlen = len(selection1[0])
    selection2 = np.where(ktdexp > 0)
    ktdexl = len(selection2[0])
    
    print 'fixed lengths:'
    print "ktdlen = ", ktdlen
    print "ktdexl = ", ktdexl
    
    print 'descriptor lists:'
    print "ktdlst = ", ktdlst[:ktdlen]
    print "ktdexp = ", ktdexp[:ktdexl]
    
    print '------------------------------'
    print "printing content of section 3:"
    print "sec3 : ", ksec3
    ecmwfbufr.buprs3(ksec3, ktdlst, ktdexp, cnames)


print "-"*50
print "BUFR decoding example"
print "-"*50

decoding_example()

print "-"*50
print "done"
print "-"*50