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
""" ICSSProperty implementation

$Id$
"""
import re
from zope import interface
from persistent import Persistent

from interfaces import ICSSProperty


class Property(object):
    interface.implements(ICSSProperty)

    title = u''
    description = u''

    def __init__(self, name, value, title='', description='', type=''):
        self.name = name
        self.value = value
        self.title = title
        self.description = description
        self.type = type

    def process(self, text):
        regex = re.compile(re.escape(self.name))
        return regex.subn(self.value, text)[0]


class CSSProperty(Property, Persistent):
    pass
