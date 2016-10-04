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


import csv
import time
import config as cfg
import helpers


def _print_datadir(datadir, errors):
    output = ''
    for ws_k, ws in enumerate(datadir['ws_list']):
        output += 'Worspaces errors: ' + str(errors['ws_errors']) + '\n'
        output += '*' * 79 + '\n'
        output += '* WS ' + str(ws_k+1) + '/' + str(datadir['ws_nb']) + ' - ' + str(ws) + ' [St. errors:' + str(errors['st_errors']) + ']' + '\n'
        output += '*' * 79 + '\n'
        for st_k, st in enumerate(datadir[ws]['st_list']):
            output += '| ST ' + str(st_k+1) + '/' + str(datadir[ws]['st_nb']) + ' - ' + str(st) + ' [Rs. errors:' + str(errors['rs_errors']) + ']' + '\n'
            output += '-' * 79 + '\n'
            for ly_k, ly in enumerate(datadir[ws][st]['ly_list']):
                layer = datadir[ws][st][ly]['obj']

                output += 'name: ' + str(layer.name) + '\n'
                output += 'title: ' + str(layer.title) + '\n'
                output += 'abstract: ' + str(layer.abstract) + '\n'
                output += 'enabled: ' + str(layer.enabled) + '\n'
                output += 'resource_type: ' + str(layer.resource_type) + '\n'
                output += 'advertised: ' + str(layer.advertised) + '\n'
                output += 'native_bbox: ' + str(layer.native_bbox) + '\n'
                output += 'latlon_bbox: ' + str(layer.latlon_bbox) + '\n'
                output += 'projection: ' + str(layer.projection) + '\n'
                output += 'projection_policy: ' + str(layer.projection_policy) + '\n'
                output += 'keywords: ' + str(layer.keywords) + '\n'
                output += 'metadata_links: ' + str(layer.metadata_links) + '\n'
                # output += 'metadata: ' + str(layer.metadata) + '\n'
                output += 'attribution: ' + str(layer.attribution) + '\n'
                output += 'default_style: ' + str(layer.default_style) + '\n'
                # For FeatureTypes (vector)
                if layer.resource_type == 'featureType':
                    output += 'native_name: ' + str(layer.native_name) + '\n'
                    output += 'attributes: ' + str(layer.attributes) + '\n'
                # For Coverages (raster)
                if layer.resource_type == 'coverage':
                    output += 'request_srs_list: ' + str(layer.request_srs_list) + '\n'
                    output += 'response_srs_list: ' + str(layer.response_srs_list) + '\n'
                    output += 'supported_formats: ' + str(layer.supported_formats) + '\n'
                # For WMS layer (wms)
                if layer.resource_type == 'wmsLayer':
                    pass

                output += '-' * 79 + '\n'
    return output


def _write_csv(datadir, filename):
    with open(filename, 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(['worspace', 'store', 'name', 'title', 'abstract', 'enabled', 'resource_type', 'advertised', 'native_bbox', 'latlon_bbox', 'projection', 'projection_policy', 'keywords', 'metadata_links', 'metadata', 'attribution', 'default_style', 'native_name', 'attributes', 'request_srs_list', 'response_srs_list', 'supported_formats'])

        for ws_k, ws in enumerate(datadir['ws_list']):
            workspace = str(ws)
            for st_k, st in enumerate(datadir[ws]['st_list']):
                store = str(st)
                for ly_k, ly in enumerate(datadir[ws][st]['ly_list']):
                    layer = datadir[ws][st][ly]['obj']

                    name = layer.name
                    title = layer.title
                    abstract = layer.abstract
                    enabled = layer.enabled
                    resource_type = layer.resource_type
                    advertised = layer.advertised
                    # native_bbox = layer.native_bbox
                    native_bbox = ''
                    if layer.native_bbox is not None:
                        for i in [0, 1, 2, 3, 4]:
                            if layer.native_bbox[i] is not None and len(layer.native_bbox[i]) < 30:
                                native_bbox += layer.native_bbox[i] + '\n'
                    # latlon_bbox = layer.latlon_bbox
                    latlon_bbox = ''
                    if layer.latlon_bbox is not None:
                        for i in [0, 1, 2, 3, 4]:
                            if layer.latlon_bbox[i] is not None:
                                if len(layer.latlon_bbox[i]) < 30:
                                    latlon_bbox += layer.latlon_bbox[i] + '\n'
                                else:
                                    latlon_bbox += 'Field too long.' + '\n'
                    projection = layer.projection
                    projection_policy = layer.projection_policy
                    # keywords = layer.keywords
                    keywords = ''
                    if layer.keywords is not None:
                        for kw in layer.keywords:
                            # keywords += kw.decode('utf-8').encode('utf-8') + '\n'
                            keywords += kw.encode('utf-8') + '\n'
                    # metadata_links = layer.metadata_links
                    metadata_links = ''
                    if layer.metadata_links is not None:
                        for md in layer.metadata_links:
                            # keywords += kw.decode('utf-8').encode('utf-8') + '\n'
                            metadata_links += ' | '.join(md) + '\n'
                    attribution = layer.attribution
                    # print layer.attribution
                    attribution = ''
                    for att_key, att_value in layer.attribution.iteritems():
                        if att_value is None:
                            att_value = ''
                        attribution += att_key + ':' + att_value + '\n'
                    default_style = layer.default_style
                    # For FeatureTypes (vector)
                    if layer.resource_type == 'featureType':
                        metadata = layer.metadata
                        native_name = layer.native_name
                        attributes = layer.attributes
                        request_srs_list = ''
                        response_srs_list = ''
                        supported_formats = ''
                    # For Coverages (raster)
                    if layer.resource_type == 'coverage':
                        metadata = layer.metadata
                        request_srs_list = layer.request_srs_list
                        response_srs_list = layer.response_srs_list
                        supported_formats = layer.supported_formats
                        native_name = ''
                        attributes = ''
                    # For WMS layer (wms)
                    if layer.resource_type == 'wmsLayer':
                        metadata = ''

                    writer.writerow([workspace, store, name, title, abstract, enabled, resource_type, advertised, native_bbox, latlon_bbox, projection, projection_policy, keywords, metadata_links, metadata, attribution, default_style, native_name, attributes, request_srs_list, response_srs_list, supported_formats])

    # print open(filename, 'rb').read()


def get_csv():
    cat = cfg.cat
    datadir, errors = helpers.get_datadir(cat)
    _write_csv(datadir, 'output_' + str(int(time.time())) + '.csv')
    # print datadir


def get_txt():
    cat = cfg.cat
    datadir, errors = helpers.get_datadir(cat)
    output = _print_datadir(datadir, errors)
    # print(datadir, errors)
    with open('output_' + str(int(time.time())) + '.txt', 'w') as file:
        file.write(output)
