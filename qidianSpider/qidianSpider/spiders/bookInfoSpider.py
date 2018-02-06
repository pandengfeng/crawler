'''
Created on 2018年2月6日

@author: Administrator
'''
import scrapy
#import logging

class bookInfoSpider(scrapy.Spider):
    name = "bookInfoSpider"
    start_urls = ["https://www.qidian.com/"]
    
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
                        self.parse,
                        meta={
                        'splash':{
                            'args':{'lua_source': self.script},
                            'endpoint': 'execute'
                            }
                        })
    
    def parse(self, response):
        
        #line 命令行测试
        from scrapy.shell import inspect_response
        inspect_response(response, self)