# coding=utf-8
from scrapy import log
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request

from lacapital.items import Article

from datetime import date, timedelta
import re

keywords = [u'asesinado', u'asesinato',  u'ejecutado',  u'ejecución',  u'disparo',  u'cabeza',  u'pecho',  u'rodilla',  u'hombre',  u'mujer',  u'arma larga',  u'arma',  u'revólver',  u'9 mm',  u'calibre',  u'luz del día',  u'moto',  u'auto',  u'balacera',  u'joven',  u'sicario',  u'narcotráfico',  u'droga',  u'cocaína',  u'paco',  u'marihuana']

def uniques(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

class LaCapitalPolicialesSpider(BaseSpider):
    name = "lacapitalpoliciales"
    allowed_domains = ["archivo.lacapital.com.ar"]

    def __init__(self, year=2003, *args, **kwargs):
        super(LaCapitalPolicialesSpider, self).__init__(*args, **kwargs)
        start_date = date(year, 1, 1)
        dates = [d for d in (start_date + timedelta(n) for n in range(366)) 
                 if d.year == year ]
        self.start_urls = [ \
            "http://archivo.lacapital.com.ar/%s/seccion_policiales.html" % \
            d.strftime("%Y/%m/%d") \
            for d in dates ]


    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        articles = uniques(hxs.select('//a[contains(@href, "articulo")]/@href')\
            .extract())
        for path in articles:
            yield Request("http://archivo.lacapital.com.ar%s" % path, 
                          callback=self.parse_article)

    def parse_article(self, response):
        self.log("Haciendo como que parseo el articulo %s" % response.url)
        hxs = HtmlXPathSelector(response)
        for k in keywords:
            if (re.search(k, hxs.extract())):
                self.log("El art. en %s contiene %s" % (response.url, k))
                title = hxs.select('//table')[5].select('.//table')[2].select('.//font')[0].select('.//font')[2].select('text()').extract()
                item = Article()
                item['title'] = title[0]
                item['url'] = response.url
                return item

        return None
