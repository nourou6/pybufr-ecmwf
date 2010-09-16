#!/usr/bin/env python

""" a small script to make it easier for me to run pylint
on the python code in the pybufr_ecmwf module"""

import sys, os
from pylint import lint

# this commandline option:
#        '--init-hook=\'import sys;sys.path.append(\"pybufr_ecmwf\")\'',
# is equivalent to:
sys.path.append("pybufr_ecmwf")

# see: the Run class in:
# /usr/lib/python2.6/site-packages/pylint/lint.py
# for examples on how to run the checkers manually

EX_PROGR_PATH = 'pybufr_ecmwf/example_programs'
EX_FILES = ['example_for_using_bufrinterface_ecmwf_for_decoding.py',
            'example_for_using_bufrinterface_ecmwf_for_encoding.py',
            'example_for_using_ecmwfbufr_for_decoding.py',
            'example_for_using_ecmwfbufr_for_encoding.py',
            'example_for_using_pb_routines.py',
            'example_for_using_rawbufrfile.py',
            'verify_bufr_tables.py']

def check(msg, pycode, additional_args):
    #  #[
    """ a little helper function to run pylint on a python
    script or module directory """
    print msg+pycode
    args = additional_args
    args.extend(['--rcfile', 'pylint/pylintrc', pycode])
    try:
        # note: the Run method always ends with a sys.exit() call
        # so the except clause seems always to be called when
        # the checking is done
        lint.Run(args)

        # this point is never reached ...
        print 'this point should not be used'
        return (-1, pycode)
    except SystemExit as sysexit:
        if (sysexit.args[0] == 0):
            print 'all seems fine'
            return (0, pycode)
        else:
            print "exception occurred; exit status: ", sysexit.args[0]
            return (1, pycode)
        
    #  #]

def check_pylint_numpy_handling():
    #  #[
    """
    a dedicated (hopefully temporary) routine to try running pylint
    on a small piece of example python code using numpy.
    This is needed to allow a workaround, because at the moment (sept-2010)
    pylint seems not able to handle the way the functions, classes and types
    are defined in the numpy module (probably because some of its class
    attributes are dynamically set?)
    """

    (success, pycode) = check('checking script: ',
                              'pylint/pylint_numpy_test.py',
                              additional_args = [])
    if (success == 0):
        use_numpy_checks = True
        return
    
    (success, pycode) = check('checking script: ',
                              'pylint/pylint_numpy_test.py',
                              additional_args=['--ignored-classes=numpy'])
    if (success == 0):
        use_numpy_checks = False
        return

    # the code should not reach this point
    print "Programming problem in check_pylint_numpy_handling:"
    print "success = ", success
    print "pycode = ", pycode
    sys.exit(1)
    #  #]

def check_all_py_files():
    #  #[
    """
    a function to find all python code in this project, and run
    the pylint checker on it.
    """

    use_numpy_checks = check_pylint_numpy_handling()
    if use_numpy_checks:
        additional_args = []
    else:
        additional_args = ['--ignored-classes=numpy']

    result = []
    #result.append(check('checking module: ', 'pybufr_ecmwf',additional_args))
    result.append(check('checking script: ', 'clean.py', additional_args))
    result.append(check('checking script: ', 'setup.py', additional_args))
    result.append(check('checking script: ', 'pylint/run_pylint.py',
                        additional_args))
    for ex_file in EX_FILES:
        result.append(check('checking script: ',
                            os.path.join(EX_PROGR_PATH, ex_file),
                            additional_args))

    num_not_ok = sum([r[0] for r in result])
    num_ok     = len(result) - num_not_ok
    
    print "done; nr of modules/scripts checked: ", len(result)
    print "number of well validated modules/scripts: ", num_ok
    print "number of problematic    modules/scripts: ", num_not_ok

    print '\n'.join('status: %2i file %s' % (i, f) for (i, f) in result)
    #  #]

check_all_py_files()
