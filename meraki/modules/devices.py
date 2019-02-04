#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from .base import Base
from .clients import Clients
from meraki.exceptions import SerialMissing


class Devices(Base):
    def __init__(self, api_key=None, parent=None):
        super(Devices, self).__init__(api_key=api_key)
        self._parent = parent
        self._name = 'devices'

        # sub endpoint
        self.clients = Clients(api_key, self._name)

    def list(self, network, serial=None):
        '''
        List the devices in a network

        OR

        Return a single device or 
        '''
        return self._get_request(self._parent, network, self._name) if serial is None else self._get_request(self._parent, network, self._name, serial)

    def update(self, network=None, serial=None, update={}):
        '''
        Update the attributes of a device
        PARAMETERS
            name:           The name of a device
            tags:           The tags of a device
            lat:            The latitude of a device
            lng:            The longitude of a device
            address:        The address of a device
            notes:          The notes for the device. String. Limited to 255 characters.
            moveMapMarker:  Whether or not to set the latitude and longitude of a device based on the new address. Only applies when lat and lng are not specified.
        '''
        self._put_request(self._parent, network, self._name, serial, update=update)


    def performance(self, network=None, serial=None):
        '''
        Return the performance score for a single device. 
        Only primary MX devices supported. 
        If no data is available, a 204 error code is returned.
        '''
        if network is None:
            raise NetworkIdMissing

        if serial is None:
            raise SerialMissing

        return self._get_request(self._parent, network, self._name, serial, 'performance')

    def uplink(self, network=None, serial=None):
        '''
        Return the uplink information for a device.
        '''
        if network is None:
            raise NetworkIdMissing

        if serial is None:
            raise SerialMissing

        return self._get_request(self._parent, network, self._name, serial, 'uplink')

    def claim(self, network=None, serial=None):
        '''
        Claim a device into a network
        '''
        if network is None:
            raise NetworkIdMissing

        if serial is None:
            raise SerialMissing

        return self._post_request(self._parent, network, self._name, 'claim', data={'serial': serial})

    def remove(self, network=None, serial=None):
        '''
        Remove a single device
        '''
        if network is None:
            raise NetworkIdMissing

        if serial is None:
            raise SerialMissing

        return self._post_request(self._parent, network, self._name, serial, 'remove')

    def lldp_cdp(self, network=None, serial=None, timespan=3600):
        '''
        List LLDP and CDP information for a device

        PARAMETERS
            timespan:   The timespan for which LLDP and CDP information will be fetched. Must be in seconds and less than or equal to a month (2592000 seconds).
        '''
        if network is None:
            raise NetworkIdMissing

        if serial is None:
            raise SerialMissing

        if timespan > 2592000:
            timespan = 2592000 

        return self._get_request(self._parent, network, self._name, serial, 'lldp_cdp', parms={'timespan': timespan})

    def loss_and_latency(self, network=None, serial=None, t0=0, t1=0, timespan=3600, resolution=60, uplink='wan1', ip=None):
        '''
        Get the uplink loss percentage and latency in milliseconds for a wired network device.
        '''
        if network is None:
            raise NetworkIdMissing

        if serial is None:
            raise SerialMissing

        if ip is None:
            raise IpMissing

        parms={
            'resolution': resolution,
            'uplink': uplink,
            'ip': ip
        }

        if t0 > 0 and t1 > 0:
            parms.update({
                't0': t0,
                't1': t1
            })
        else:
            parms.update({
                'timespan': timespan
            })

        return self._get_request(self._parent, network, self._name, serial, 'lossAndLatencyHistory', parms=parms)
