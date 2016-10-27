#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""get_styles.py module
Post sld from a directorie and specify workspace 
"""

__author__ = "Jean-Pascal Klipfel"
__copyright__ = "Copyright 2016, Jean-pascal Klipfel"
__credits__ = ["Jean-pascal Klipfel"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Jean-pascal Klipfel"
__email__ = "jean-pascal.klipfel@region-alsace.org"
__status__ = "Developement"

import config as cfg
import helpers
import os

def run():
    config = cfg.config
    cat = cfg.cat
    log = []
    sld_dir = config['config']['sld_dir']
    ws = config['config']['ws_post_styles']
    for root, dirs, filenames in os.walk(sld_dir):
        for sld in filenames:
            fullpath = os.path.join(sld_dir, sld)
            with open(fullpath) as f:
                cat.create_style(sld[:-4], f.read(), overwrite=False, workspace=ws)
                
    print '\n'.join(log)