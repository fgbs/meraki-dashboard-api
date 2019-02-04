#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys

from meraki.modules import *
from meraki.exceptions import ApiKeyMissing

class Dashboard(object):
    def __init__(self, api_key=None):
        if api_key is None:
            raise ApiKeyMissing

        self._api_key = api_key
        self._baseurl = None  # override base_url with shard node

    def __getattr__(self, name):
        if 'meraki.modules.{}'.format(name) not in sys.modules:
            message = 'module meraki has no attribute {name!r}'
            raise AttributeError(message)

        module = sys.modules['meraki.modules.{}'.format(name)]
        klass = module.__dict__[name.capitalize()]

        if klass is not None:
            return klass(self._api_key)
