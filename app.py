# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 02:11:41 2016

"""

import os
#!/user/bin/env python

from spyre.server import Site, App

from country import CountryApp
from language import LanguageApp
from correlation import CorrelationApp
from digitalSource import DigitalSourceApp


class Index(App):
    def getHTML(self, params):
        return "Title Page Here"


#site = Site(Index)

site = Site(CountryApp)

site.addApp(LanguageApp, '/app2')
site.addApp(CorrelationApp, '/app2/app3')
site.addApp(DigitalSourceApp, '/app2/app3/app4')


site.launch()