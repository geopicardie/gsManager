#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""gsManager.py module

Main file of gsManager application.
"""

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2015, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume.ryckelynck@region-alsace.org"
__status__ = "Developement"


import sys
import time
import processes
import importlib

# Encoding management
if sys.version_info[0] < 3:
    reload(sys) # Reload does the trick!
    sys.setdefaultencoding('UTF8')
else:
    importlib.reload(sys)


if __name__ == '__main__':
    # Get script duration
    start_time = time.time()

    # Manage args
    total = len(sys.argv)
    if total > 1:
        for arg in sys.argv[1:]:
            process = str(arg)
            processes.lst[process]()
    else:
        print('No process specified')

    # Print script duration
    print("--- %s seconds ---" % (time.time() - start_time))
