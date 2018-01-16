'''
Created on 2018年1月15日

@author: Administrator
'''
import sys
sys.path
import scrapy
from myfirst.items import BdtbItem

class BdtbSpider(scrapy.Spider):
    name = "bdtbSpider"
    allowed_domains  = ["tieba.baidu.com"]
    start_urls = ["http://tieba.baidu.com/f/index/forumpark?pcn=%E5%8A%A8%E6%BC%AB%E5%AE%85&pci=206&ct=0&rn=20&pn=1"]
    def parse(self, response):
        item = BdtbItem()
        for box in response.xpath("//div[contains(@class,'ba_info')]"):
            item['title'] = box.xpath(".//p[@class='ba_name']/text()").extract_first();
            item['message'] = box.xpath(".//p[@class='ba_desc']/text()").extract_first();
            item['url'] = "http://tieba.baidu.com"+box.xpath(".//a[contains(@class,'ba_href')]/@href").extract_first();
            item['image'] = box.xpath(".//img[@class='ba_pic']/@src").extract_first();
            item['userNum'] = box.xpath(".//span[@class='ba_m_num']/text()").extract_first();
            item['postNum'] = box.xpath(".//span[@class='ba_p_num']/text()").extract_first();
            yield item
        nextUrl = response.xpath("//div[@class='pagination']/a[@class='next']/@href").extract_first();
        if nextUrl:
            nextUrl = "http://tieba.baidu.com"+ nextUrl
            yield scrapy.Request(nextUrl,callback=self.parse)