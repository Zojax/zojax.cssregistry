============
CSS Registry
============

A registry for linked Stylesheet files and Javascripts.

This registry is mainly aimed at solving the following usecases:

  - Enable skin developer to change css properties without having to 
    resort to override css files itself
    
  - Enable more componentialization of the stylesheets.

Some usefull imports

   >>> from zope import interface, component
   >>> from zope.interface.verify import verifyObject
   >>> from zojax.cssregistry.interfaces import \
   ...   Layer, ICSSRegistry, ICSSRegistryLayer

   >>> from zope.publisher.browser import TestRequest
   >>> request = TestRequest()

Load directive declaration

   >>> from zope.configuration import xmlconfig
   >>> context = xmlconfig.string("""
   ... <configure>
   ...    <include package="zojax.cssregistry" file="meta.zcml" />
   ... </configure>""")

Now we can create css registry

   >>> context = xmlconfig.string("""
   ... <configure xmlns:browser="http://namespaces.zope.org/browser">
   ...   <browser:cssregistry>
   ...      <property name="color1" value="#f5f5f5" />
   ...      <property name="color2" value="white" />
   ...      <property name="fontFamilyH1" value="Verdana" />
   ...      <property name="fontFamilyH2" value="Arial" />
   ...   </browser:cssregistry>
   ... </configure>""", context)

`browser:cssregistry` diretive creates ICSSRegistry. It accepts name,title,layer 
parameters. All parameters not required, by default registry will have blank name
and registered against IDefaultBrowserLayer layer. We can't register cssregistry
for layer, because in that case it whould be available as resource (++resource++)
So directive register multi adapter for ICSSRegistryLayer and supplied layer

   >>> registry = component.getMultiAdapter((Layer, Layer, request), ICSSRegistry)
   >>> verifyObject(ICSSRegistry, registry)
   True

   >>> registry['color1'].value
   u'#f5f5f5'

   >>> registry['fontFamilyH1'].value
   u'Verdana'

We also can add more properties later:

   >>> context = xmlconfig.string("""
   ... <configure xmlns:browser="http://namespaces.zope.org/browser">
   ...   <browser:cssproperty name="color3" value="#225593" />
   ... </configure>""", context)

   >>> registry['color3'].value
   u'#225593'


zrt command
-----------

zojax.cssregistry package aslo register new command for z3c.zrtresource.

   >>> from zojax.cssregistry.command import cssregistry_factory
   >>> from z3c.zrtresource.interfaces import IZRTCommandFactory

   >>> component.provideUtility(cssregistry_factory, IZRTCommandFactory, 'cssregistry')

Now we can use cssregistry for zrtresource resources

   >>> import tempfile
   >>> fn = tempfile.mktemp('.css')
   >>> open(fn, 'w').write('''\
   ... /* zrt-cssregistry: */
   ... h1 {
   ...   color: color1;
   ...   font: fontFamilyH1;
   ... }
   ...
   ... h2 {
   ...   color: color2;
   ...   font: fontFamilyH2;
   ... }''')

   >>> from z3c.zrtresource.zrtresource import ZRTFileResourceFactory
   >>> cssFactory = ZRTFileResourceFactory(fn, None, 'site.css')

   >>> from zope.publisher.browser import TestRequest
   >>> css = cssFactory(TestRequest())

   >>> print css.GET()
   h1 {
     color: #f5f5f5;
     font: Verdana;
   }
   <BLANKLINE>
   h2 {
     color: white;
     font: Arial;
   }

Now if we need change css file we only need change cssregistry properties

   >>> registry['color1'].value = 'black'

   >>> print css.GET()
   h1 {
     color: black;
     font: Verdana;
   }
   <BLANKLINE>
   h2 {
     color: white;
     font: Arial;
   }

We also can use named cssregistries

   >>> context = xmlconfig.string("""
   ... <configure xmlns:browser="http://namespaces.zope.org/browser">
   ...   <browser:cssregistry name="mycss">
   ...      <property name="color1" value="#d5d5d5" />
   ...      <property name="color2" value="black" />
   ...      <property name="fontFamilyH1" value="Tahoma" />
   ...      <property name="fontFamilyH2" value="Courier" />
   ...   </browser:cssregistry>
   ... </configure>""", context)

   >>> open(fn, 'w').write('''\
   ... /* zrt-cssregistry: mycss */
   ... h1 {
   ...   color: color1;
   ...   font: fontFamilyH1;
   ... }
   ...
   ... h2 {
   ...   color: color2;
   ...   font: fontFamilyH2;
   ... }''')

   >>> print css.GET()
   h1 {
     color: #d5d5d5;
     font: Tahoma;
   }
   <BLANKLINE>
   h2 {
     color: black;
     font: Courier;
   }

If cssregistry is unknown nothing will happen

   >>> open(fn, 'w').write('''\
   ... /* zrt-cssregistry: unknown */
   ... h1 {
   ...   color: color1;
   ...   font: fontFamilyH1;
   ... }''')
   >>> print css.GET()
   h1 {
     color: color1;
     font: fontFamilyH1;
   }


Registry methods
----------------

   >>> registry.keys()
   [u'color1', u'color3', u'color2', u'fontFamilyH2', u'fontFamilyH1']

   >>> list(iter(registry))
   [u'color1', u'color3', u'color2', u'fontFamilyH2', u'fontFamilyH1']

   >>> for key, prop in registry.items():
   ...     print key, prop
   color1 <zojax.cssregistry.property.Property ...>
   color3 <zojax.cssregistry.property.Property ...>
   color2 <zojax.cssregistry.property.Property ...>
   fontFamilyH2 <zojax.cssregistry.property.Property ...>
   fontFamilyH1 <zojax.cssregistry.property.Property ...>

   >>> len(registry)
   5

   >>> u'color1' in registry
   True

   >>> registry.get(u'color1')
   <zojax.cssregistry.property.Property ...>

   >>> del registry[u'color1']
   >>> registry.keys()
   [u'color3', u'color2', u'fontFamilyH2', u'fontFamilyH1']
