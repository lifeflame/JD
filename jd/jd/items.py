# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field

class JdItem(Item):
    # define the fields for your item here like:
    phone_name = Field()  #定义手机名字
    store = Field() #定义商店名称
    price = Field() #定义手机价格
    comment_num = Field() #定义评论数量
    link = Field() #每条信息的链接地址

class Jdcomment(Item):
    comment = Field() #定义评论
    score = Field() #定义评论星级


