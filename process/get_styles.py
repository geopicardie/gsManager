#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""get_styles.py module
Dowload all sld files from a workspace
Do not work for global sld)
"""

__author__ = "Jean-Pascal Klipfel"
__copyright__ = "Copyright 2016, Jean-pascal Klipfel"
__credits__ = ["Jean-pascal Klipfel"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Jean-pascal Klipfel"
__email__ = "jean-pascal.klipfel@region-alsace.org"
__status__ = "Developement"

import urlparse
import config as cfg
import helpers
import base64
import urllib2

def run():
    config = cfg.config
    cat = cfg.cat
    log = []
    workspaces, ws_errors = helpers.get_workspaces(cat, config['config']['gs_ws_include'], config['config']['gs_ws_exclude'])
    for ws in workspaces:
         stores, st_errors = helpers.get_stores(cat, ws.name)
         for st in stores:
            resources, rs_errors = helpers.get_resources(cat, ws.name, st.name)
            md_id = None
            for rs in resources:
                ly = cat.get_layer(rs.name)
                rs.default_style = ly.default_style
                url = config['config']['_gs_url'] + '/workspaces/' + ws.name + '/styles/' + rs.default_style.name + '.sld'
                print 'add --> ' + url
                user, password = config['config']['gs_username'], config['config']['gs_password']
                try:
                    request = urllib2.Request(url)
                    base64string = base64.b64encode('%s:%s' % (user, password))
                    request.add_header("Authorization", "Basic %s" % base64string)
                    result = urllib2.urlopen(request)
                    with open(rs.default_style.name + '.sld', "wb") as code:
                        code.write(result.read())
                except urllib2.HTTPError as e:
                    error_message = e.read()
                    print error_message
                
    print '\n'.join(log)