# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import csv
import os

class JdPipeline(object):

    def __init__(self):
        #连接数据库，创建游标
        self.db = pymysql.connect(host="localhost",user='root',password="xxxxxx",port=3306,db='crawlspider')
        self.cur = self.db.cursor()

    def process_item(self, item, spider):
        sql = "INSERT INTO jingdong(phone_name,store,comment_num,price) VALUES(%s,%s,%s,%s)"
        try:
            self.db.ping(reconnect=True)
            self.cur.execute(sql, (item["phone_name"],item["store"],item["comment_num"],item["price"]))
            self.db.commit()
        except:
            self.db.rollback()
        finally:
            self.db.close()

        return item

class Jdcommentpipiline(object):

    def open_spider(self,spider):
        os.chdir("D:\crawl picture")
        self.file = open("jd.csv","w",newline="")
        self.writer = csv.writer(self.file)

    def process_item(self, item1, spider):
        self.writer.writerows(item1["comment"])

    def close_spider(self,spider):
        self.file.close()


