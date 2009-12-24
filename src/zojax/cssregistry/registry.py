##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface
from interfaces import ICSSRegistry

registries = {}


class CSSRegistry(object):
    interface.implements(ICSSRegistry)

    @property
    def properties(self):
        try:
            return self._properties
        except AttributeError:
            self._properties = {}
            return self._properties

    def keys(self):
        return self.properties.keys()

    def __iter__(self):
        return iter(self.properties)

    def values(self):
        return self.properties.values()

    def items(self):
        return self.properties.items()

    def __len__(self):
        return len(self.properties)

    def __setitem__(self, key, value):
        self.properties[key] = value

    def __getitem__(self, key):
        return self.properties[key]

    def __delitem__(self, key):
        del self.properties[key]

    def get(self, key, default=None):
        return self.properties.get(key, default)

    def __contains__(self, key):
        return key in self.properties
