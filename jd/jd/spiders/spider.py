import scrapy
import json
from scrapy import Spider
from ..items import JdItem
from..items import Jdcomment


class Jd_spider(Spider):
    #设置name,该name在爬虫中唯一
    name = "jd"
    #设置爬取域名
    allowed_domains = ["jd.com"]
    #获取入口url
    start_urls = []
    # for i in range(100):
    for i in range(3):
        url = "https://search.jd.com/Search?keyword=手机&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=手机&cid2=653&cid3=655&page=%d"%(2*i+1)
        start_urls.append(url)

    def parse(self,response):
        #提取出每一页所有的货物标签
        goods = response.xpath("//div[@id='J_goodsList']/ul/li")
        for good in goods:
            #提取出需要的手机名称，手机店铺，评论数，价格
            item = JdItem()
            item["phone_name"] = "".join(good.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()").extract()).strip()
            store = good.xpath("./div/div[@class='p-shop']/span/a/@title")
            if store.extract():
                item["store"] = store.extract()[0]
            item["comment_num"] = good.xpath(".//div[@class='p-commit']/strong/a/text()").extract()[0]
            price = good.xpath(".//div[@class='p-price']/strong/i/text()")
            if price.extract():
                item["price"] = price.extract()[0]
            base_url = good.xpath(".//div[@class='p-name p-name-type-2']/a/@href").extract()[0]
            url = "https:"+base_url
            # print(item)
            yield scrapy.Request(url,callback=self.get_comment,meta={"url":base_url},dont_filter=False)
            return item

    def get_comment(self,response):
        base_url = response.meta["url"]
        try:
            for i in range(1,3):
                productid = base_url.split("/")[-1].strip(".html")
                url = "https://sclub.jd.com/comment/productPageComments.action?productId="+str(productid)+"&score=0&sortType=5&page="+str(i)+"&pageSize=10"
                yield scrapy.Request(url,callback=self.content,dont_filter=False)
        except:
            print("error")

    def content(self,response):
        #加载存储的json文件
        js = json.loads(response.body_as_unicode())
        if js.get("comment"):
            comments = js["comments"]
            for each in comments:
                item1 = Jdcomment()
                #实例化item,将星级和评论存储在item中
                content = each["content"]
                score = each["score"]
                item1["comment"] = content
                item1["score"] = score
                # print(item1)
                return item1




