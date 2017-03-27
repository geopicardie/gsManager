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
import sys
if sys.version_info[0] < 3:
    from urlparse import urlparse, parse_qs
else:
    from urllib.parse import urlparse, parse_qs
import config as cfg
import helpers
import re
import requests

from neogeo_xml_utils import XMLtoObj
from xml.etree.ElementTree import XMLParser

from requests.auth import HTTPBasicAuth

def run():
    config = cfg.config
    cat = cfg.cat
    log = []
    workspaces, ws_errors = helpers.get_workspaces(cat, config['config']['gs_ws_include'], config['config']['gs_ws_exclude'])
    for ws in workspaces:
        log.append('> WORKSPACE: ' + ws.name)
        stores, st_errors = helpers.get_stores(cat, ws.name)
        for st in stores:
            log.append(' ' * 2 + '* STORE: ' + st.name)
            resources, rs_errors = helpers.get_resources(cat, ws.name, st.name)
            md_id = None
            for rs in resources:
                log.append(' ' * 4 + '- Layer: ' + rs.name)
                missing = None
                # if ('metadata_links' in rs):

                try:
                    md_links = rs.metadata_links
                    if md_links is not None:
                        missing = ['tc211_html', 'tc211_xml', 'iso19115_html', 'iso19115_xml']
                        md_url = urlparse(rs.metadata_links[0][2])
                        md_id = parse_qs(md_url.query)['uuid'][0]

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
                        md_id = None
                        log.append(' ' * 4 + '- MD link: ' + 'NO METADATA LINK')
                except:
                    log.append(' ' * 4 + '- MD link: ' + 'ERROR')

                if md_id is not None and missing is not None:
                    for m in missing:
                        if m == 'tc211_html':
                            log.append(' ' * 4 + '=> Add tc211/html')
                            md_links.append(('text/html', 'TC211', 'https://www.geopicardie.fr/geonetwork/apps/georchestra/?uuid=' + md_id))
                        elif m == 'tc211_xml':
                            log.append(' ' * 4 + '=> Add iso19115:2003/html')
                            md_links.append(('text/xml', 'TC211', 'https://www.geopicardie.fr/geonetwork/srv/fre/xml_iso19139?uuid=' + md_id))
                        elif m == 'iso19115_html':
                            log.append(' ' * 4 + '=> Add tc211/xml')
                            md_links.append(('text/html', 'ISO19115:2003', 'https://www.geopicardie.fr/geonetwork/apps/georchestra/?uuid=' + md_id))
                        elif m == 'iso19115_xml':
                            log.append(' ' * 4 + '=> Add iso19115:2003/html')
                            md_links.append(('text/xml', 'ISO19115:2003', 'https://www.geopicardie.fr/geonetwork/srv/fre/xml_iso19139?uuid=' + md_id))
                    rs.metadata_links = md_links
                    cat.save(rs)


                if md_id is not None:
                    res = None
                    log.append(' ' * 4 + 'ANALYSE OnlineResources dans la fiche de métadonnée ' + md_id)
                    #Vérification des URLs liées dans la fiche de MD
                    try:
                        md_url = 'https://www.geopicardie.fr/geonetwork/srv/fre/xml_iso19139?uuid=' + md_id
                        user, password = config['config']['gs_username'], config['config']['gs_password']
                        r = requests.get(md_url, auth=(user, password))
                        target = XMLtoObj(attrib_tag='@', text_tag='_')
                        parser = XMLParser(target=target)
                        parser.feed(r.text)
                        res = parser.close()

                    except:
                        log.append(' ' * 4 + '- Impossible de parser ' + md_url)

                    if res is not None:
                        try:
                            onlineResources = res['MD_Metadata']['distributionInfo']['MD_Distribution']['transferOptions']['MD_DigitalTransferOptions']['onLine']

                        except:
                            log.append(' ' * 4 + '- Section "MD_DigitalTransferOptions > onLine" non trouvée pour ' + rs.name)
                            onlineResources = None


                        if onlineResources is not None:
                            cpt = 0
                            for resource in onlineResources:
                                try :
                                    protocol = resource['CI_OnlineResource']['protocol']['CharacterString']
                                except :
                                    #log.append(' ' * 4 + '- WARNING : "CI_OnlineResource > protocol" non trouvé dans le bloc analysé')
                                    continue

                                # On ne traite que les protocoles WxS
                                s = re.search('w(m|f|mt|c)s', protocol, flags=re.I)
                                if s is None:
                                    continue

                                try:
                                    linkage = resource['CI_OnlineResource']['linkage']['URL']
                                except :
                                    log.append(' ' * 4 + '- WARNING : "CI_OnlineResource > linkage" non trouvé dans le bloc analysé')
                                    continue

                                cpt += 1
                                log.append(' ' * 4 + '- OnlineResource URL : ' + protocol + ' | ' + linkage)
                                if 'GetCapabilities' not in linkage:
                                    log.append(' ' * 6 + '* ERROR : manque GetCapabilities')

                                try:
                                    l_name = resource['CI_OnlineResource']['name']['CharacterString']
                                except :
                                    log.append(' ' * 6 + '* WARNING : "CI_OnlineResource > name" non trouvé dans le bloc analysé')
                                    continue

                                if l_name not in (rs.name, ws.name + ':' + rs.name):
                                    log.append(' ' * 6 + '* ERROR : name différent du layer : ' + l_name)

                            if cpt == 0:
                                log.append(' ' * 4 + '- Aucun service WFS, WMS, WCS ou WMTS détecté dans cette fiche')

                log.append('-' * 79)

    print('\n'.join(log))
