#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from .base import Base


class Admins(Base):
    def __init__(self, api_key=None, parent=None):
        super(Admins, self).__init__(api_key=api_key)
        self._parent = parent
        self._name = 'admins'

    def list(self, org=None):
        '''
        List the dashboard administrators in this organization
        '''
        return self._get_request(self._parent, org, self._name)

    def create(self, org=None, data={}):
        '''
        Create a new dashboard administrator
        '''
        return self._post_request(self._parent, org, self._name, data=data)

    def update(self, org=None, admin=None, update={}):
        '''
        Update an administrator
        '''
        return self._post_request(self._parent, org, self._name, admin, update=update)

    def delete(self, org=None, admin=None):
        '''
        Revoke all access for a dashboard administrator within this organization
        '''
        return self._del_request(self._parent, org, self._name, admin)

