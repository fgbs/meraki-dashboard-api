#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from .base import Base
from .clients import Clients
from .devices import Devices
from .ssids import Ssids
from meraki.exceptions import NetworkIdMissing, IpMissing, ClientIdMissing, MacAddressMissing, DevicePolicyMissing, SerialMissing


class Networks(Base):
    def __init__(self, api_key=None):
        super(Networks, self).__init__(api_key=api_key)
        self._name = 'networks'
        
        # sub endpoint
        self.clients = Clients(api_key, self._name)
        self.devices = Devices(api_key, self._name)
        self.ssids = Ssids(api_key, self._name)

    def list(self, id=None):
        '''
        Return a network
        '''
        if id is None:
            raise NetworkIdMissing

        return self._get_request(self._name, id)

    def create(self, name=None, type=None, tags=[], time_zone='America/Los_Angeles', copy_from_network=None, disable_my_meraki_com=False, disable_remote_status_page=False):
        '''
        Create a network

        PARAMETERS
            name:                       The name of the new network
            type:                       The type of the new network. Valid types are wireless, appliance, switch, phone, systemsManager, camera or a space-separated list of those for a combined network.
            tags:                       A space-separated list of tags to be applied to the network
            timeZone:                   The timezone of the network.
            copyFromNetworkId:          The ID of the network to copy configuration from. Other provided parameters will override the copied configuration, except type which must match this network's type exactly.
            disableMyMerakiCom:         Disables the local device status pages (my.meraki.com, ap.meraki.com, switch.meraki.com, wired.meraki.com). Optional (defaults to false)
            disableRemoteStatusPage:    Disables access to the device status page (http://[device's LAN IP]). Optional. Can only be set if disableMyMerakiCom is set to false
        '''

        data = {
            'name': name,
            'type': ' '.join(type),
            'tags': ' '.join(tags),
            'timeZone': time_zone,
            'disableMyMerakiCom': disable_my_meraki_com,
            'disableRemoteStatusPage': disable_remote_status_page
        }

        if copy_from_network is not None:
            data.update({
                'copyFromNetworkId': copy_from_network
            })
        
        return self._post_request(self._name, id, data=data)

    def update(self, id, name=None, time_zone='America/Los_Angeles', tags=[], disable_my_meraki_com=False, disable_remote_status_page=False):
        '''
        Update network

        PARAMETERS
            name:                       The name of the new network
            timeZone:                   The timezone of the network.
            tags:                       A space-separated list of tags to be applied to the network
            disableMyMerakiCom:         Disables the local device status pages (my.meraki.com, ap.meraki.com, switch.meraki.com, wired.meraki.com). Optional (defaults to false)
            disableRemoteStatusPage:    Disables access to the device status page (http://[device's LAN IP]). Optional. Can only be set if disableMyMerakiCom is set to false
        '''
        if id is None:
            raise NetworkIdMissing

        update = {
            'name': name,
            'timeZone': time_zone,
            'tags': ' '.join(tags),
            'disableMyMerakiCom': disable_my_meraki_com,
            'disableRemoteStatusPage': disable_remote_status_page
        }

        return self._put_request(self._name, id, update=update)
    
    def delete(self, id=None):
        '''
        Delete a network
        '''
        if id is None:
            raise NetworkIdMissing

        return self._del_request(self._name, id)

    def bind_template(self, id=None, config_template=None, auto_bind=False):
        '''
        Bind a network to a template.

        PARAMETERS
            configTemplateId:   The ID of the template to which the network should be bound.
            autoBind:           Optional boolean indicating whether the network's switches should automatically bind to profiles of the same model. Defaults to false
        '''
        if id is None:
            raise NetworkIdMissing

        data = {
            'configTemplateId': config_template,
            'autoBind': auto_bind
        }

        return self._post_request(self._name, id, 'bind', data=data)


    def unbind_template(self, id=None):
        '''
        Unbind a network from a template.
        '''
        if id is None:
            raise NetworkIdMissing

        return self._post_request(self._name, id, 'unbind', data={})


    def sts_vpn(self, id=None, mode=None, hubs=[], subnets=[]):
        '''
        Return the site-to-site VPN settings of a network. Only valid for MX networks.

        OR

        Update the site-to-site VPN settings of a network. Only valid for MX networks in NAT mode.
        '''
        if id is None:
            raise NetworkIdMissing

        if mode is None and len(hubs) == 0 and len(subnets) == 0:
            update = {
                'mode': mode,
                'hubs': hubs,
                'subnets': subnets
            }
            return self._put_request(self._name, id, 'siteToSiteVpn', update=update)
        else:
            return self._get_request(self._name, id, 'siteToSiteVpn')

    def traffic(self, id=None, timespan=3600):
        '''
        The traffic analysis data for this network. 
        
        Traffic Analysis with Hostname Visibility must be enabled on the network.
        '''
        if id is None:
            raise NetworkIdMissing

        if timespan > 2592000:
            timespan = 2592000 

        return self._get_request(self._name, id, 'traffic', parms={'timespan': timespan})

    def access_polices(self, id=None):
        '''
        List the access policies for this network. Only valid for MS networks.
        '''
        if id is None:
            raise NetworkIdMissing

        return self._get_request(self._name, id, 'accessPolicies')

    def air_marshal(self, id=None):
        '''
        List Air Marshal scan results from a network
        '''
        if id is None:
            raise NetworkIdMissing

        if timespan > 2592000:
            timespan = 2592000 

        return self._get_request(self._name, id, 'airMarshal', parms={'timespan': timespan})

    def bluetooth_settings(self, id=None, scanning_enabled=False, advertising_enabled=False, uuid=None, major_minor_assignment_mode=None, major=0, minor=0):
        '''
        Return the Bluetooth settings for a network. Bluetooth settings must be enabled on the network.

        OR

        Update the Bluetooth settings for a network. See the docs page for Bluetooth settings.

        PARAMETERS
            scanningEnabled:            Whether APs will scan for Bluetooth enabled clients. (true, false)
            advertisingEnabled:         Whether APs will advertise beacons. (true, false)
            uuid:                       The UUID to be used in the beacon identifier.
            majorMinorAssignmentMode:   The way major and minor number should be assigned to nodes in the network. ('Unique', 'Non-unique')
            major:                      The major number to be used in the beacon identifier. Only valid in 'Non-unique' mode.
            minor:                      The minor number to be used in the beacon identifier. Only valid in 'Non-unique' mode.
        '''
        if id is None:
            raise NetworkIdMissing

        if scanning_enabled or advertising_enabled:
            update = {
                'scanningEnabled': scanning_enabled,
                'advertisingEnabled': advertising_enabled,
                'majorMinorAssignmentMode': major_minor_assignment_mode
            }

            if major_minor_assignment_mode == 'Non-unique':
                update.update({
                    'major': major,
                    'minor': minor
                })

            return self._put_request(self._name, id, 'bluetoothSettings', update=update)
        else:
            return self._get_request(self._name, id, 'bluetoothSettings')

    #
    # ALERTS
    #

    def alert_settings(self, network=None, default_destinations=None, alerts=[]):
        '''
        Return the alert configuration for this network

        OR

        Update the alert configuration for this network

        PARAMETERS
            defaultDestinations:    The network_wide destinations for all alerts on the network.
                emails:     A list of emails that will recieve the alert(s).
                allAdmins:  If true, then all network admins will receive emails.
                snmp:       If true, then an SNMP trap will be sent if there is an SNMP trap server configured for this network.

            alerts:                 Alert-specific configuration for each type. Only alerts that pertain to the network can be updated.
                type:               The type of alert
                enabled:            A boolean depicting if the alert is turned on or off
                alertDestinations:  A hash of destinations for this specific alert. Keys include: emails: A list of emails that will recieve information about the alert, allAdmins: If true, then all network admins will receive emails, and snmp: If true, then an SNMP trap will be sent if there is an SNMP trap server configured for this network.
                filters:            A hash of specific configuration data for the alert. Only filters specific to the alert will be updated.
        '''
        if network is None:
            raise NetworkIdMissing

        if default_destinations is not None:
            update = {
                'defaultDestinations': default_destinations,
                'alerts': alerts
            }

            return self._put_request(self._name, network, 'alertSettings', update=update)
        else:
            return self._get_request(self._name, network, 'alertSettings')

    #
    # bluetooth clients
    #

    def bluetooth_clients(self, network=None, client=None, timespan=3600, include_connectivity_history=False, per_page=30):
        '''
        List the Bluetooth clients seen by APs in this network

        PARAMETERS
            timespan:                   The timespan, in seconds, used to look back from now for bluetooth clients
            includeConnectivityHistory: Include the connectivity history for this client
            perPage:                    The number of entries per page returned
            startingAfter:              A token used by the server to indicate the start of the page. Often this is a timestamp or an ID but it is not limited to those. This parameter should not be defined by client applications. The link for the first, last, next or prev page in the HTTP Link header should define it.
            endingBefore:               A token used by the server to indicate the end of the page. Often this is a timestamp or an ID but it is not limited to those. This parameter should not be defined by client applications. The link for the first, last, next or prev page in the HTTP Link header should define it.
        '''
        if network is None:
            raise NetworkIdMissing

        if timespan > 2592000:
            timespan = 2592000 

        if client is not None:
            parms = {
                'includeConnectivityHistory': include_connectivity_history,
                'connectivityHistoryTimespan': timespan
            }

            return self._get_request(self._name, network, 'bluetoothClients', client, parms=parms)
        else:
            parms = {
                'timespan': timespan,
                'includeConnectivityHistory': include_connectivity_history,
                'perPage': per_page
            }

            return self._get_request(self._name, network, 'bluetoothClients', parms=parms)

    #
    # splash
    #
    def splash_login_attempts(self, network=None, ssid=None, timespan=3600):
        '''
        List the splash login attempts for a network
        '''
        if timespan > 2592000:
            timespan = 2592000 

        parms = {
            'timespan': timespan
        }

        if ssid is not None:
            parms.update({
                'ssidNumber': str(ssid)
            })

        return self._get_request(self._name, network, 'splashLoginAttempts', parms=parms)
