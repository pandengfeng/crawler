'''
Created on 2018年2月6日

@author: Administrator
'''
import scrapy
#import logging
from qidianSpider.items import BookDetailInfo
from qidianSpider.items import BookTags
#import time  
import datetime 

class bookInfoSpider(scrapy.Spider):
    name = "bookInfoSpider"
    start_urls = ["https://www.qidian.com/all?page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0"]
    base_url = "https://www.qidian.com"
    book_info_base_url = "https://book.qidian.com/info/"
    #私有配置项
    custom_settings = {
        'LOG_FILE': 'scrapy.log',
        'LOG_STDOUT':True
    }
    #lua脚本
    script = """
           function main(splash, args)
              splash.images_enabled = false
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
                        self.parse_all_book,
                        meta={
                        'splash':{
                            'args':{'lua_source': self.script},
                            'endpoint': 'execute'
                            }
                        })
    #首页parse
    def parse_all_book(self, response):
        #刮取开始
        elementSelect = response.xpath("//ul[@class='all-img-list cf']")
        bookBaseSelects = elementSelect.xpath(".//li")
        for bookBaseSelect in bookBaseSelects:
            book_url = bookBaseSelect.xpath(".//div[@class='book-mid-info']//a//@data-bid").extract_first()
            #book_name = bookBaseSelect.xpath(".//div[@class='book-mid-info']//a//text()").extract_first()
            #logging.info("书名:"+book_name+"URL:"+book_url)
            #书籍详细信息
            url = self.book_info_base_url + book_url
            #logging.info("url:"+url)
            yield scrapy.Request(url,
                        self.parse_detail_book,
                        meta={
                        'splash':{
                            'args':{'lua_source': self.script},
                            'endpoint': 'execute'
                            }
                        })
        
        
        
        """    
        #下一页
        nextUrl = response.xpath("//a[@class='lbf-pagination-next']//@href").extract_first()   
         
        if nextUrl:
            #下一页操作
            nextUrl = "https" + nextUrl
            yield  scrapy.Request(nextUrl,
                        self.parse_all_book,
                        meta={
                        'splash':{
                            'args':{'lua_source': self.script},
                            'endpoint': 'execute'
                            }
                        }) 
        """  
        #line 命令行测试
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
    #书籍详细信息  
    def parse_detail_book(self,response):
        #详细
        bookDetailInfo = BookDetailInfo()
        #标签
        bookTags = BookTags()
        
        
        book_info_element = response.xpath("//div[@class='book-info ']")
        
        #作品id
        book_id = response.xpath("//div[@class='book-img']//a//@data-bid").extract_first()
        
        bookDetailInfo['book_id'] = book_id
        #作品名称
        bookDetailInfo['book_name'] = book_info_element.xpath(".//h1//em//text()").extract_first()
        #作者
        bookDetailInfo['book_author'] = book_info_element.xpath(".//h1//span//a//text()").extract_first()
        
        #数据部分element
        book_info_detail_element =  book_info_element.xpath(".//p")[2]
        
        #总数据
        data_sum_num =   book_info_detail_element.xpath(".//em//text()").extract() 

        #字数
        bookDetailInfo['book_words_number'] = data_sum_num[0] * 10000
        #点击量
        bookDetailInfo['book_click_quantity'] = data_sum_num[1] * 10000
        #推荐数
        bookDetailInfo['book_recommend_number'] = data_sum_num[2]
        #月票数
        bookDetailInfo['book_monthly_ticket_number'] = response.xpath("//i[@id='monthCount']//text()").extract_first()
        #如果没有 置 0
        if(bookDetailInfo['book_monthly_ticket_number']):
            bookDetailInfo['book_monthly_ticket_number'] = 0
        #打赏数
        bookDetailInfo['book_support_number'] = response.xpath("//i[@id='rewardNum']//text()").extract_first()
        #简介
        bookDetailInfo['book_introduction'] = response.xpath("string(//div[@class='book-intro']//p)").extract_first()
    
        #作品页面链接
        bookDetailInfo['book_page_url'] = self.book_info_base_url + book_id
        
        str_time = response.xpath("//em[@class='time']//text()").extract_first()[0:2]
        update_time = None
        if str_time == '今天':
            update_time = datetime.datetime.now()
            #格式化时间
            update_time = update_time.strftime("%Y-%m-%d %H:%M:%S")  
        elif str_time == '昨日':
            oneday=datetime.timedelta(days=1) 
            update_time = datetime.datetime.today() - oneday
            #格式化时间
            update_time = update_time.strftime("%Y-%m-%d %H:%M:%S") 
        else:
            update_time = str_time       
        #最近更新时间
        bookDetailInfo['book_near_update_time'] = update_time
        
        #章节数  ----加载缓慢 可能数据丢失
        book_chapter_number= response.xpath("//span[@id='J-catalogCount']//text()").extract_first()
        if book_chapter_number:
            bookDetailInfo['book_chapter_number'] = book_chapter_number[1:-2]
        else:
            bookDetailInfo['book_chapter_number'] = 0
            
        #讨论数 ----加载缓慢 可能数据丢失
        book_discuss_number = response.xpath("//span[@id='J-discusCount']//text()").extract_first()
        if book_discuss_number:
            bookDetailInfo['book_discuss_number'] = book_discuss_number[1:-2]
        else:
            bookDetailInfo['book_chapter_number'] = 0
        yield bookDetailInfo 
        
        
        bookTags['book_id'] = book_id
        #作品标签
        book_tags = book_info_element.xpath(".//p[@class='tag']//span//text()").extract()
        
        for book_tag in book_tags:
            #保存到标签表
            bookTags['book_tag'] = book_tag
            yield bookTags

        book_tags = book_info_element.xpath(".//p[@class='tag']//a//text()").extract()
        
        for book_tag in book_tags:
            #保存到标签表
            bookTags['book_tag'] = book_tag
            yield bookTags
        

