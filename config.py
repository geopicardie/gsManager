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

import json
import geoserver.catalog

config_file = 'config.json'

# Load config file
with open(config_file, 'r') as cfg:
    config = json.loads(cfg.read())

# Get Geoserver datadir catalog connexion
cat = geoserver.catalog.Catalog(config['config']['gs_url'], config['config']['gs_username'], config['config']['gs_password'], disable_ssl_certificate_validation=config['config']['gs_disable_certificate'])
