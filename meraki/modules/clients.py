#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from .base import Base
from meraki.exceptions import NetworkIdMissing, ClientIdMissing, MacAddressMissing, DevicePolicyMissing


class Clients(Base):
    def __init__(self, api_key=None, parent=None):
        super(Clients, self).__init__(api_key=api_key)
        self._parent = parent
        self._name = 'clients'

    def list(self, serial=None, timespan=3600):
        '''
        List the clients of a device, up to a maximum of a month ago. 
        The usage of each client is returned in kilobytes. 
        If the device is a switch, the switchport is returned; otherwise the switchport field is null.
        '''
        if timespan > 2592000:
            timespan = 2592000 

        return self._get_request(self._parent, serial, self._name, parms={'timespan': timespan})

    def get(self, network=None, client=None):
        '''
        Return the client associated with the given identifier. 
        This endpoint will lookup by client ID or either the MAC or IP depending on whether the network uses Track-by-IP.
        '''
        if network is None:
            raise NetworkIdMissing

        if client is None:
            raise ClientIdMissing

        return self._get_request(self._parent, network, self._name, client)

    def provision(self, network=None, mac=None, name='', device_policy=None, group_policy=None):
        '''
        Provisions a client with a name and policy. Clients can be provisioned before they associate to the network.

        PARAMETERS
            mac:            The MAC address of the client. Required.
            name:           The display name for the client. Optional. Limited to 255 bytes.
            devicePolicy:   The policy to apply to the specified client. Can be Whitelisted, Blocked, Normal, and Group policy. Required.
            groupPolicyId:  The ID of the desired group policy to apply to the client. Required if 'devicePolicy' is set to "Group policy". Otherwise this is ignored.
        '''
        if network is None:
            raise NetworkIdMissing

        if mac is None:
            raise MacAddressMissing

        if device_policy is None:
            raise DevicePolicyMissing

        data = {
            'mac': mac,
            'name': name,
            'devicePolicy': device_policy
        }

        if device_policy == 'Group policy':
            data.update({
                'groupPolicyId': group_policy
            })

        return self._post_request(self._parent, network, self._name, 'provision', data=data)

    def usage_history(self, network=None, client=None):
        '''
        Return the client's daily usage history. Usage data is in kilobytes.
        '''
        if network is None:
            raise NetworkIdMissing

        if client is None:
            raise ClientIdMissing

        return self._get_request(self._parent, network, self._name, client, 'usageHistory')

    def traffic_history(self, network=None, client=None, per_page=30):
        '''
        Return the client's network traffic data over time. 
        Usage data is in kilobytes. 
        This endpoint requires detailed traffic analysis to be enabled on the Network-wide > General page.

        PARAMETERS
            perPage:        The number of entries per page returned
            startingAfter:  A token used by the server to indicate the start of the page. Often this is a timestamp or an ID but it is not limited to those. This parameter should not be defined by client applications. The link for the first, last, next or prev page in the HTTP Link header should define it.
            endingBefore:   A token used by the server to indicate the end of the page. Often this is a timestamp or an ID but it is not limited to those. This parameter should not be defined by client applications. The link for the first, last, next or prev page in the HTTP Link header should define it.
        '''
        if network is None:
            raise NetworkIdMissing

        if client is None:
            raise ClientIdMissing

        return self._get_request(self._parent, network, self._name, client, 'trafficHistory', parms={'perPage': per_page})

    def events(self, network=None, client=None, per_page=30):
        '''
        Return the events associated with this client.
        '''
        if network is None:
            raise NetworkIdMissing

        if client is None:
            raise ClientIdMissing

        return self._get_request(self._parent, network, self._name, client, 'events', parms={'perPage': per_page})

    def security_events(self, network=None, client=None, timespan=3600, per_page=30):
        '''
        Return the events associated with this client.
        '''
        if network is None:
            raise NetworkIdMissing

        if client is None:
            raise ClientIdMissing

        if timespan > 2592000:
            timespan = 2592000 

        return self._get_request(self._parent, network, self._name, client, 'securityEvents', parms={'timespan': timespan, 'perPage': per_page})

    def latency_history(self, network=None, client=None, t0=0, t1=0, timespan=3600):
        '''
        Return the latency history for a client. 
        The latency data is from a sample of 2% of packets and is grouped into 4 traffic categories: background, best effort, video, voice. 
        Within these categories the sampled packet counters are bucketed by latency in milliseconds.
        '''
        if network is None:
            raise NetworkIdMissing

        if client is None:
            raise ClientIdMissing

        parms = {}

        if t0 > 0 and t1 > 0:
            parms.update({
                't0': t0,
                't1': t1
            })
        else:
            parms.update({
                'timespan': timespan
            })

        return self._get_request(self._parent, network, self._name, client, 'latencyHistory', parms=parms)

    def policy(self, network=None, client=None, device_policy=None, group_policy=None, timespan=3600):
        '''
        Return the policy assigned to a client on the network.

        OR

        Update the policy assigned to a client on the network.

        PARAMETERS
            devicePolicy:   The group policy (Whitelisted, Blocked, Normal, Group policy)
            groupPolicyId:  If devicePolicy param is set to 'Group policy' this param is used to specify the group ID.
            timespan:       The timespan for which clients will be fetched. Must be in seconds and less than or equal to a month (2592000 seconds).
        '''
        if network is None:
            raise NetworkIdMissing

        if client is None:
            raise MacAddressMissing

        if timespan > 2592000:
            timespan = 2592000 

        parms = {
            'timespan': timespan
        }

        if device_policy == 'Group policy':
            parms.update({
                'devicePolicy': device_policy,
                'groupPolicyId': group_policy
            })
        elif device_policy is not None:
            parms.update({
                'devicePolicy': device_policy
            })

        return self._get_request(self._parent, network, self._name, client, 'policy', parms=parms)

    def splash_auth_status(self, network=None, client=None, ssid=None, is_authorized=False):
        '''
        Return the splash authorization for a client, for each SSID they've associated with through splash.

        OR

        Update a client's splash authorization.

        PARAMETERS
            ssids:  The target SSIDs. For each SSID where isAuthorized is true, the expiration time will 
                    automatically be set according to the SSID's splash frequency.  
                    
                    isAuthorized: New authorization status for SSID (true, false).
        '''
        if network is None:
            raise NetworkIdMissing

        if client is None:
            raise MacAddressMissing

        if ssid is not None:
            update = {
                'ssids': {
                    ssid: {'isAuthorized': is_authorized}
                }
            }
            return self._put_request(self._parent, network, self._name, client, 'splashAuthorizationStatus', update=update)
        else:
            return self._get_request(self._parent, network, self._name, client, 'splashAuthorizationStatus')



