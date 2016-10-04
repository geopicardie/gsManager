#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""check_mdlinks.py module

check_mdlinks process function.
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
import urlparse
import config as cfg
import helpers


def run():
    config = cfg.config
    cat = cfg.cat
    log = []
    workspaces, ws_errors = helpers.get_workspaces(cat, config['config']['gs_ws_include'], config['config']['gs_ws_exclude'])
    for ws in workspaces:
        log.append('> WOKSPACE: ' + ws.name)
        stores, st_errors = helpers.get_stores(cat, ws.name)
        for st in stores:
            log.append(' ' * 2 + '* STRORE: ' + st.name)
            resources, rs_errors = helpers.get_resources(cat, ws.name, st.name)
            md_id = None
            for rs in resources:
                log.append(' ' * 4 + '- Layer: ' + rs.name)
                missing = None
                # if ('metadata_links' in rs):
                try:
                    # print rs.metadata_links
                    # log.append('ok');
                    md_links = rs.metadata_links
                    if md_links is not None:
                        missing = ['tc211_html', 'tc211_xml', 'iso19115_html', 'iso19115_xml']
                        md_url = urlparse.urlparse(rs.metadata_links[0][2])
                        md_id = urlparse.parse_qs(md_url.query)['uuid'][0]
                        for md in rs.metadata_links:
                            log.append(' ' * 4 + '- MD link: ' + ' | '.join(md))
                            if md[0] == 'text/html':
                                if md[1] == 'TC211':
                                    missing.remove('tc211_html')
                                elif md[1] == 'ISO19115:2003':
                                    missing.remove('iso19115_html')
                            elif md[0] == 'text/xml':
                                if md[1] == 'TC211':
                                    missing.remove('tc211_xml')
                                elif md[1] == 'ISO19115:2003':
                                    missing.remove('iso19115_xml')
                    else:
                        log.append(' ' * 4 + '- MD link: ' + 'NO METADATA LINK')
                except:
                    log.append(' ' * 4 + '- MD link: ' + 'ERROR')

                if md_id is not None and missing is not None:
                    for m in missing:
                        if m == 'tc211_html':
                            log.append(' ' * 4 + '=> Add tc211/html')
                            md_links.append(('text/html', 'TC211', 'https://www.cigalsace.org/geonetwork/apps/georchestra/?uuid=' + md_id))
                        elif m == 'tc211_xml':
                            log.append(' ' * 4 + '=> Add iso19115:2003/html')
                            md_links.append(('text/xml', 'TC211', 'https://www.cigalsace.org/geonetwork/srv/fre/xml_iso19139?uuid=' + md_id))
                        elif m == 'iso19115_html':
                            log.append(' ' * 4 + '=> Add tc211/xml')
                            md_links.append(('text/html', 'ISO19115:2003', 'https://www.cigalsace.org/geonetwork/apps/georchestra/?uuid=' + md_id))
                        elif m == 'iso19115_xml':
                            log.append(' ' * 4 + '=> Add iso19115:2003/html')
                            md_links.append(('text/xml', 'ISO19115:2003', 'https://www.cigalsace.org/geonetwork/srv/fre/xml_iso19139?uuid=' + md_id))
                    rs.metadata_links = md_links
                    cat.save(rs)
                log.append('-' * 79)

    print '\n'.join(log)
