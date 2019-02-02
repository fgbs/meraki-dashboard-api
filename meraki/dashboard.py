#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import ssl
import json
from requests import Session, Request
from requests_toolbelt import SSLAdapter

# workaround to suppress InsecureRequestWarning
# See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings
import urllib3
urllib3.disable_warnings()

import exceptions
from modules import *


class Dashboard(object):
    def __init__(self, api_key=None):
        if api_key is None:
            raise exceptions.ApiKeyMissing

        self._api_key = api_key
        self._baseurl = None  # override base_url with shard node

    def __getattr__(self, name):
        if 'modules.{}'.format(name) not in sys.modules:
            message = 'module meraki has no attribute {name!r}'
            raise AttributeError(message)

        module = sys.modules['modules.{}'.format(name)]
        klass = module.__dict__[name.capitalize()]

        if klass is not None:
            return klass(self._api_key)
