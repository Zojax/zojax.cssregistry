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
""" z3c.zrtresource zrt-cssregistry command implementation

$Id$
"""
import re
from zope import interface
from zope.proxy import removeAllProxies
from zope.component import factory, queryUtility, queryMultiAdapter

from z3c.zrtresource.interfaces import IZRTCommand, IZRTCommandFactory

from interfaces import Layer, ICSSRegistry


class CSSRegistryCommand(object):
    interface.implements(IZRTCommand)

    isAvailable = True

    def __init__(self, args, start, end):
        self.start = start
        self.end = end
        self.name = args.strip()

    def process(self, text, context, request):
        registry = queryMultiAdapter(
            (Layer, request), ICSSRegistry, name=self.name)

        if registry is None:
            registry = queryMultiAdapter(
                (Layer, Layer, request), ICSSRegistry, name=self.name)

        if registry is None:
            return text
        for property in removeAllProxies(registry).values():
            text = property.process(text)

        return text


cssregistry_factory = factory.Factory(CSSRegistryCommand, 'cssregistry')
interface.directlyProvides(cssregistry_factory, IZRTCommandFactory)
