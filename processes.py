#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""processes.py module

List of processes functions.
"""

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2015, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume.ryckelynck@region-alsace.org"
__status__ = "Developement"


# import csv
# import urlparse
# import config as cfg
# import helpers
import process.datadir
import process.check_mdlinks
import process.get_styles
import process.post_styles

def p1():
    print('hello')


def help():
    print ('Liste des process disponibles:')
    for p in lst:
        print('- ' + p)


lst = {
    'p1': p1,
    'help': help,
    'get_csv': process.datadir.get_csv,
    'get_txt': process.datadir.get_txt,
    'check_mdlinks': process.check_mdlinks.run,
    'get_styles': process.get_styles.run,
    'post_styles': process.post_styles.run
}
