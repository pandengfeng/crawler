'''
Created on 2018年2月6日

@author: Administrator
'''
import scrapy
from scrapy.commands import fetch
#import logging

class bookInfoSpider(scrapy.Spider):
    name = "bookInfoSpider"
    start_urls = ["https://www.qidian.com/"]
    base_url = "https://www.qidian.com"
    #lua脚本
    script = """
           function main(splash, args)
              assert(splash:go(args.url))
              assert(splash:wait(0.5))
              return {
                html = splash:html(),
              }
        end
    """
    def start_requests(self):
        for url in self.start_urls:
            #起步url请求 调用splash 渲染js
            yield  scrapy.Request(url,
                        self.parse_index,
                        meta={
                        'splash':{
                            'args':{'lua_source': self.script},
                            'endpoint': 'execute'
                            }
                        })
    #首页parse
    def parse_index(self, response):
        #分类url
        classify_list  = response.xpath("//div[@id='classify-list']//dd")
        #分类url 遍历
        for classify in classify_list:
            #分类url拼接基础url
            classify  = self.base_url + classify.xpath(".//@href").extract_first()
            yield  scrapy.Request(classify,
                        self.parse_classify_page,
                        meta={
                        'splash':{
                            'args':{'lua_source': self.script},
                            'endpoint': 'execute'
                            }
                        })
            
    #分类页面 parse
    def parse_classify_page(self,response):
        #line 命令行测试
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        
        