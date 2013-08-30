# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

# class LacapitalItem(Item):
#     # define the fields for your item here like:
#     # name = Field()
#     pass

class Article(Item):
    title = Field()
    url = Field()
    desc = Field()

