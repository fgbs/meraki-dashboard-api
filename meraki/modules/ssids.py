#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from .base import Base


class Ssids(Base):
    def __init__(self, api_key=None, parent=None):
        super(Ssids, self).__init__(api_key=api_key)
        self._parent = parent
        self._name = 'ssids'

    def list(self, network=None):
        '''
        List the SSIDs in a network. Supports networks with access points or wireless-enabled security appliances and teleworker gateways.
        '''
        return self._get_request(self._parent, network, self._name)
    
    def get(self, network=None, ssid=None):
        '''
        Return a single SSID
        '''
        return self._get_request(self._parent, network, self._name, ssid)

    def update(self, network=None, ssid=None, update={}):
        '''
        Update the attributes of an SSID
        '''
        return self._put_request(self._parent, network, self._name, ssid, update=update)
    
    def splash_settings(self, network=None, ssid=None, update={}):
        '''
        Display the splash page settings for the given SSID

        OR

        Modify the splash page settings for the given SSID
        '''
        if len(update) == 0:
            return self._get_request(self._parent, network, self._name, ssid, 'splashSettings')
        else:
            return self._put_request(self._parent, network, self._name, ssid, 'splashSettings', update=update)
