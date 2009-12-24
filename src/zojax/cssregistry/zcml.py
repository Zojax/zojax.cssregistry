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
""" `browser:cssregistry` directive

$Id$
"""

from zope import schema, interface
from zope.component.zcml import handler
from zope.configuration.fields import MessageID, GlobalObject

from property import Property
from registry import CSSRegistry, registries

from interfaces import _, ICSSRegistry, ICSSRegistryLayer


class ICSSRegistryDirective(interface.Interface):

    name = schema.TextLine(
        title = u'Name',
        description = u'Registry name',
        required = False)

    title = schema.TextLine(
        title = u'Title',
        required = False)

    layer = GlobalObject(
        title = u"The layer the css registry should be found in",
        required = False)


class ICSSPropertySubDirective(interface.Interface):

    name = schema.TextLine(
        title = u'Name',
        description = u'Property name',
        required = True)

    value = schema.TextLine(
        title = u'Value',
        description = u'Property value',
        required = True)

    title = MessageID(
        title = u'Title',
        description = u'Property title',
        required = False)

    description = MessageID(
        title = u'Description',
        description = u'Property description',
        required = False)

    type = schema.TextLine(
        title = u'Type',
        description = u'Property type. (color, font, size)',
        required = False)


class ICSSPropertyDirective(interface.Interface):

    registry = schema.TextLine(
        title = u'Registry',
        required = False)

    layer = GlobalObject(
        title = u"The layer the css registry should be found in",
        required=False)

    name = schema.TextLine(
        title = u'Name',
        required = True)

    value = schema.TextLine(
        title = u'Value',
        required = True)

    description = schema.TextLine(
        title = u'Description',
        description = u'Property description',
        required = False)

    type = schema.TextLine(
        title = u'Type',
        description = u'Property type. (color, font, size)',
        required = False)


class Factory(object):

    def __init__(self, registry):
        self.registry = registry

    def __call__(self, layer1, layer2, request):
        return self.registry


class cssregistryHandler(object):

    def __init__(self, _context, name='', title='', layer=interface.Interface):
        self.name = name
        self.layer = layer

        self.registry = CSSRegistry()
        self.registry.name = name
        self.registry.title = title

        registries[(name, layer)] = self.registry

        # we can't use just 'layer', because registry will be registered as resource
        _context.action(
            discriminator = ('CSSRegistry', name, layer),
            callable = handler,
            args = ('registerAdapter',
                    Factory(self.registry),
                    (ICSSRegistryLayer, ICSSRegistryLayer, layer),
                    ICSSRegistry, name, _context.info),
            )

    def property(self, _context, name, value,
                 title=u'', description='', type=''):
        self.registry[name] = Property(name, value, title, description, type)


def csspropertyHandler(_context, name, value, registry='',
                       layer=interface.Interface,
                       title='', description='', type=''):
    registry = registries[(registry, layer)]
    registry[name] = Property(name, value, title, description, type)
