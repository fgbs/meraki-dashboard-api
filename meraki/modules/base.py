#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import ssl
import json
from requests import Session, Request
from requests_toolbelt import SSLAdapter

# workaround to suppress InsecureRequestWarning
# See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
import urllib3
urllib3.disable_warnings()

from meraki.exceptions import ApiKeyMissing, APIError


class Base(object):
    def __init__(self, api_key=None):
        if api_key is None:
            raise ApiKeyMissing

        self._api_key = api_key
        self._baseurl = 'https://api.meraki.com/api/v0'
        self._headers = {
            'X-Cisco-Meraki-API-Key': str(self._api_key),
            'Content-type': 'application/json'
        }
        
        self._session = Session()
        self._session.mount(self._baseurl, SSLAdapter(ssl.PROTOCOL_SSLv23))

    def _bulid_url(self, *args, **kwargs):
        url = '{}/{}'.format(
            self._baseurl,
            args[0]
        )

        if len(args) > 1:
            extra = '/'.join(args[1:])
            url = '{}/{}'.format(url, extra)

        # print('DEBUG URL:', args, kwargs)
        # print('DEBUG URL:', url)

        return url

    def _build_querystring(self, url, **kwargs):
        if not len(kwargs):
            return url
        
        args = []
        for key in kwargs['parms']:
            args.append('{}={}'.format(key, kwargs['parms'][key]))

        query = '&'.join(args)

        # print('DEBUG Q:', kwargs['parms'])
        # print('DEBUG Q:', query)

        return '{}?{}'.format(url, query)


    def _jsondec(self, data):
        if data.ok:
            return data.json()
        else:
            return {
                'status': data.status_code,
                'reason': data.reason
            }

    def _get_request(self, *args, **kwargs):
        return self._jsondec(
            self._session.send(
                self._session.prepare_request(
                    Request(
                        'GET',
                        self._build_querystring(
                            self._bulid_url(*args), **kwargs
                        ),
                        headers=self._headers
                    )
                ),
                verify=False
            )
        )

    def _post_request(self, *args, **kwargs):
        return self._jsondec(
            self._session.send(
                self._session.prepare_request(
                    Request(
                        'POST',
                        self._bulid_url(*args),
                        data=json.dumps(kwargs['data']).encode('utf8'),
                        headers=self._headers
                    )
                ),
                verify=False
            )
        )

    def _put_request(self, *args, **kwargs):
        return self._jsondec(
            self._session.send(
                self._session.prepare_request(
                    Request(
                        'PUT',
                        self._bulid_url(*args),
                        data=json.dumps(kwargs['update']).encode('utf8'),
                        headers=self._headers
                    )
                ),
                verify=False
            )
        )

    def _del_request(self, *args, **kwargs):
        return self._jsondec(
            self._session.send(
                self._session.prepare_request(
                    Request(
                        'DELETE',
                        self._bulid_url(args),
                        headers=self._headers
                    )
                ),
                verify=False
            )
        )
