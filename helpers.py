#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""helpers.py module

Helpers functions.
"""

__author__ = "Guillaume Ryckelynck"
__copyright__ = "Copyright 2015, Guillaume Ryckelynck"
__credits__ = ["Guillaume Ryckelynck"]
__license__ = "MIT"
__version__ = "0.01"
__maintainer__ = "Guillaume Ryckelynck"
__email__ = "guillaume.ryckelynck@region-alsace.org"
__status__ = "Developement"

import config as cfg

config = cfg.config
# cat = cfg.cat


def get_workspaces(cat, include, exclude):
    workspaces = []
    errors = 0
    all_workspaces = cat.get_workspaces()
    try:
        for ws in all_workspaces:
            if len(config['config']['gs_ws_include']):
                if ws.name in config['config']['gs_ws_include']:
                    workspaces.append(ws)
            else:
                if ws.name not in config['config']['gs_ws_exclude']:
                    workspaces.append(ws)
    except:
        errors += 1
    return workspaces, errors


def get_stores(cat, ws_name):
    stores = []
    errors = 0
    try:
        all_stores = cat.get_stores(workspace=ws_name)
        for st in all_stores:
            stores.append(st)
    except:
        errors += 1
    return stores, errors


def get_resources(cat, ws_name, st_name):
    resources = []
    errors = 0
    try:
        all_resources = cat.get_resources(store=st_name, workspace=ws_name)
        for rs in all_resources:
            resources.append(rs)
    except:
        errors += 1
    return resources, errors


def get_datadir(cat):
    datadir = {}
    datadir['ws_list'] = []
    workspaces, ws_errors = get_workspaces(cat, config['config']['gs_ws_include'], config['config']['gs_ws_exclude'])
    for ws in workspaces:
        # print ws.name
        datadir['ws_list'].append(ws.name)
        datadir['ws_nb'] = len(workspaces)
        datadir[ws.name] = {}
        datadir[ws.name]['ws'] = ws
        datadir[ws.name]['st_list'] = []
        stores, st_errors = get_stores(cat, ws.name)
        for st in stores:
            # print st.name
            datadir[ws.name]['st_list'].append(st.name)
            datadir[ws.name]['st_nb'] = len(stores)
            datadir[ws.name][st.name] = {}
            datadir[ws.name][st.name]['st'] = st
            datadir[ws.name][st.name]['ly_list'] = []
            resources, rs_errors = get_resources(cat, ws.name, st.name)
            for rs in resources:
                # print rs.name, rs.title
                datadir[ws.name][st.name]['ly_list'].append(rs.name)
                datadir[ws.name][st.name]['ly_nb'] = len(resources)
                ly = cat.get_layer(rs.name)
                rs.attribution = ly.attribution
                rs.default_style = ly.default_style
                datadir[ws.name][st.name][rs.name] = {}
                datadir[ws.name][st.name][rs.name]['obj'] = rs
                datadir[ws.name][st.name][rs.name]['dict'] = {}

                datadir[ws.name][st.name][rs.name]['dict']['name'] = str(rs.name)
                datadir[ws.name][st.name][rs.name]['dict']['title'] = str(rs.title)
                datadir[ws.name][st.name][rs.name]['dict']['abstract'] = str(rs.abstract)
                datadir[ws.name][st.name][rs.name]['dict']['enabled'] = str(rs.enabled)
                datadir[ws.name][st.name][rs.name]['dict']['resource_type'] = str(rs.resource_type)
                datadir[ws.name][st.name][rs.name]['dict']['advertised'] = str(rs.advertised)
                datadir[ws.name][st.name][rs.name]['dict']['native_bbox'] = str(rs.native_bbox)
                datadir[ws.name][st.name][rs.name]['dict']['latlon_bbox'] = str(rs.latlon_bbox)
                datadir[ws.name][st.name][rs.name]['dict']['projection'] = str(rs.projection)
                datadir[ws.name][st.name][rs.name]['dict']['projection_policy'] = str(rs.projection_policy)
                datadir[ws.name][st.name][rs.name]['dict']['keywords'] = str(rs.keywords)
                datadir[ws.name][st.name][rs.name]['dict']['metadata_links'] = str(rs.metadata_links)
                datadir[ws.name][st.name][rs.name]['dict']['attribution'] = str(rs.attribution)
                datadir[ws.name][st.name][rs.name]['dict']['default_style'] = str(rs.default_style)
                # For FeatureTypes (vector)
                if rs.resource_type == 'featureType':
                    datadir[ws.name][st.name][rs.name]['dict']['metadata'] = str(rs.metadata)
                    datadir[ws.name][st.name][rs.name]['dict']['native_name'] = str(rs.native_name)
                    datadir[ws.name][st.name][rs.name]['dict']['attributes'] = str(rs.attributes)
                    datadir[ws.name][st.name][rs.name]['dict']['request_srs_list'] = ''
                    datadir[ws.name][st.name][rs.name]['dict']['response_srs_list'] = ''
                    datadir[ws.name][st.name][rs.name]['dict']['supported_formats'] = ''
                # For Coverages (raster)
                if rs.resource_type == 'coverage':
                    datadir[ws.name][st.name][rs.name]['dict']['metadata'] = str(rs.metadata)
                    datadir[ws.name][st.name][rs.name]['dict']['request_srs_list'] = str(rs.request_srs_list)
                    datadir[ws.name][st.name][rs.name]['dict']['response_srs_list'] = str(rs.response_srs_list)
                    datadir[ws.name][st.name][rs.name]['dict']['supported_formats'] = str(rs.supported_formats)
                    datadir[ws.name][st.name][rs.name]['dict']['native_name'] = ''
                    datadir[ws.name][st.name][rs.name]['dict']['attributes'] = ''
                # For WMS layer (wms)
                if rs.resource_type == 'wmsLayer':
                    datadir[ws.name][st.name][rs.name]['dict']['metadata'] = ''

    return datadir, {'ws_errors': ws_errors, 'st_errors': st_errors, 'rs_errors': rs_errors}
