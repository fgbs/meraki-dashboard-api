#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from .base import Base


class Organizations(Base):
    def __init__(self, api_key=None):
        super(Organizations, self).__init__(api_key=api_key)
        self._name = 'organizations'

    def list(self, id=None):
        '''
        List the organizations that the user has privileges on

            GET /organizations

        Return an organization

            GET /organizations/[id]

        '''
        return self._get_request(self._name) if id is None else self._get_request(self._name, id)

    def networks(self, id):
        return self._get_request(self._name, id, 'networks')

    def update(self, *args, **kwargs):
        pass

    def create(self):
        pass
    
    def clone(self):
        pass

    def claim(self):
        pass

    def license_state(self):
        pass

    def inventory(self):
        pass
    
    def device_statuses(self):
        pass
    
    def snmp(self):
        pass
    
    def vpn(self):
        pass
