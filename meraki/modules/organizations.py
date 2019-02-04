#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from .base import Base
from .admins import Admins

class Organizations(Base):
    def __init__(self, api_key=None):
        super(Organizations, self).__init__(api_key=api_key)
        self._name = 'organizations'

        # sub endpoint
        self.admins = Admins(api_key, self._name)

    def list(self, org=None):
        '''
        List the organizations that the user has privileges on

        OR

        Return an organization
        '''
        return self._get_request(self._name) if org is None else self._get_request(self._name, org)

    def create(self, data={}):
        '''
        Create a new organization
        '''
        return self._post_request(self._name, data=data)
    
    def update(self, org=None, update={}):
        '''
        Update an organization
        '''
        return self._put_request(self._name, org, update=update)

    def clone(self, org=None, data={}):
        '''
        Create a new organization by cloning the addressed organization
        '''
        return self._post_request(self._name, org, 'clone', data=data)

    def claim(self, org=None, data={}):
        '''
        Claim a device, license key, or order into an organization. 
        When claiming by order, all devices and licenses in the order will be claimed; 
        licenses will be added to the organization and devices will be placed in the organization's inventory. 
        These three types of claims are mutually exclusive and cannot be performed in one request.
        '''
        return self._post_request(self._name, org, 'claim', data=data)

    def license_state(self, org=None):
        '''
        Return the license state for an organization
        '''
        return self._get_request(self._name, org, 'licenseState')        

    def inventory(self, org=None):
        '''
        Return the inventory for an organization
        '''
        return self._get_request(self._name, org, 'inventory')        
    
    def device_statuses(self, org=None):
        '''
        List the status of every Meraki device in the organization
        '''
        return self._get_request(self._name, org, 'deviceStatuses')
    
    def snmp(self, org=None, update={}):
        '''
        Return the SNMP settings for an organization

        OR

        Update the SNMP settings for an organization
        '''
        if len(update) == 0:
            return self._put_request(self._name, org, 'snmp', update=update)
        else:
            return self._get_request(self._name, org, 'snmp')
    
    def third_party_vpn_peers(self, org=None, update={}):
        '''
        Return the third party VPN peers for an organization

        OR

        Update the third party VPN peers for an organization
        '''
        if len(update) == 0:
            return self._put_request(self._name, org, 'thirdPartyVPNPeers', update=update)
        else:
            return self._get_request(self._name, org, 'thirdPartyVPNPeers')

    def networks(self, org=None):
        return self._get_request(self._name, org, 'networks')
