#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


class APIError(Exception):
    pass

class ConnectionError(Exception):
    pass

class ApiKeyMissing(Exception):
    def __init__(self):
        Exception.__init__(self, 'Meraki API Key missing.')

class ParameterMissing(Exception):
    def __init__(self, message):
        super().__init__(message)
    
class NetworkIdMissing(Exception):
    def __init__(self):
        Exception.__init__(self, 'If you need all networks, use organizations.networks(<orgId>)')

class IpMissing(Exception):
    def __init__(self):
        Exception.__init__(self, 'The destination IP used to obtain the requested stats is required.')

class ClientIdMissing(Exception):
    def __init__(self):
        Exception.__init__(self, 'client ID, MAC or IP is required.')

class MacAddressMissing(Exception):
    def __init__(self):
        Exception.__init__(self, 'MAC Address is required.')

class DevicePolicyMissing(Exception):
    def __init__(self):
        Exception.__init__(self, 'Can be Whitelisted, Blocked, Normal, and Group policy, is required.')

class SerialMissing(Exception):
    def __init__(self):
        Exception.__init__(self, 'Device serial is required.')
