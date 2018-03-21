'''
Created on 2018年2月6日

@author: Administrator
'''
import scrapy
import logging
from qidianSpider.items import BookDetailInfo
from qidianSpider.items import BookTags 
from qidianSpider.items import BookAuthor
from qidianSpider.items import BookRead
from qidianSpider.items import BookReaderPayDetail
import json
#import time  
import datetime 

#作品信息爬虫
class bookInfoSpider(scrapy.Spider):
    name = "bookInfoSpider"
    start_urls = ["https://www.qidian.com/all?page=1&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=0"]
    base_url = "https://www.qidian.com"
    book_info_base_url = "https://book.qidian.com/info/"
    
    try_again_num = 0
    
    page_num = 0
    #私有配置项
    custom_settings = {
        'LOG_FILE': 'scrapy.log',
        'LOG_STDOUT':True,
        'LOG_LEVEL':'WARNING'
    }
    
    
    logger = logging.getLogger()
    #lua脚本
    script = """
           function main(splash, args)
              splash.images_enabled = false
              assert(splash:go(args.url))
              assert(splash:wait(5))
              return {
                html = splash:html(),
              }
        end
    """
    def start_requests(self):
        
        #读取 作者 书籍信息
        for url in self.start_urls:
            #起步url请求 调用splash 渲染js
            yield  scrapy.Request(url,
                        self.parse_all_book
                      )
    #首页parse
    def parse_all_book(self, response):
        
        #下一页
        nextUrl = response.xpath("//a[@class='lbf-pagination-next ']//@href").extract_first()   
        
        #重试10次操作 
        if nextUrl:
            self.try_again_num = 0
            #下一页操作
            nextUrl = "https:" + nextUrl
            yield  scrapy.Request(nextUrl,
                        self.parse_all_book) 
        else:
            self.try_again_num = self.try_again_num + 1
            if self.try_again_num > 10:
                self.logger.warning("*************重试失败链接****************:"+str(response.url))
                self.logger.warning("当前页面page_num"+str(self.page_num))
                return
            else:
                self.logger.warning("*************开始重试****************:"+str(response.url)+",次数:"+str(self.try_again_num))
                yield scrapy.Request(response.url,
                        self.parse_all_book)
                return
        
        #页面数+1
        self.page_num = self.page_num + 1
        
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
                        self.parse_detail_book)
        
        
        #line 命令行测试
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
    #书籍详细信息  
    def parse_detail_book(self,response):
        #详细
        bookDetailInfo = BookDetailInfo()
        #标签
        bookTags = BookTags()
        
        #token cookies 
        csrfToken = str(response.request.headers['Cookie'])[13:53]
        
        book_info_element = response.xpath("//div[@class='book-info ']")
        
        #作品id
        book_id = response.xpath("//div[@class='book-img']//a//@data-bid").extract_first()
        
        bookDetailInfo['book_id'] = book_id
        #作品名称
        bookDetailInfo['book_name'] = book_info_element.xpath(".//h1//em//text()").extract_first()
        #作者
        bookDetailInfo['book_author'] = book_info_element.xpath(".//h1//span//a//text()").extract_first()
        #作者页面url
        bookDetailInfo['book_author_url'] =  "https:"+ book_info_element.xpath(".//h1//span//a//@href").extract_first()
        #数据部分element
        book_info_detail_element =  book_info_element.xpath(".//p")[2]
        
        #总数据
        data_sum_num =   book_info_detail_element.xpath(".//em//text()").extract() 

        #字数
        bookDetailInfo['book_words_number'] = data_sum_num[0]
        #点击量
        bookDetailInfo['book_click_quantity'] = data_sum_num[1]
        #推荐数
        bookDetailInfo['book_recommend_number'] = data_sum_num[2]
        #月票数
        bookDetailInfo['book_monthly_ticket_number'] = response.xpath("//i[@id='monthCount']//text()").extract_first()
        #如果没有 置 0
        if(bookDetailInfo['book_monthly_ticket_number']):
            pass
        else: 
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
            update_time = response.xpath("//em[@class='time']//text()").extract_first()    
        #最近更新时间
        bookDetailInfo['book_near_update_time'] = update_time
        #章节数  ----加载缓慢 可能数据丢失
        book_chapter_number= response.xpath("//span[@id='J-catalogCount']//text()").extract_first()
        if book_chapter_number:
            bookDetailInfo['book_chapter_number'] = book_chapter_number[1:-2]
        else:
            bookDetailInfo['book_chapter_number'] = 0
        """   
        #讨论数 ----加载缓慢 可能数据丢失
        book_discuss_number = response.xpath("//span[@id='J-discusCount']//text()").extract_first()
        if book_discuss_number:
            bookDetailInfo['book_discuss_number'] = book_discuss_number[1:-2]
        else:
        kwyYzVewq18yi1ISV3ZXdbnn20dhIbos533VWdUe
            bookDetailInfo['book_discuss_number'] = 0
        """   
        yield bookDetailInfo
  
        url = "https://book.qidian.com/ajax/book/GetBookForum?_csrfToken="+csrfToken+"&authorId="+str(book_info_element.xpath(".//h1//span//a//@href").extract_first()[36:])+"&bookId="+str(book_id)+"&chanId=12&pageSize=0"
        #讨论数
        yield scrapy.Request(url,self.parse_book_threadList) 
        
        #章节数 0 清楚 ajax查询
        if bookDetailInfo['book_chapter_number'] == 0:
            book_chapter_number_url = "https://book.qidian.com/ajax/book/category?_csrfToken="+csrfToken+"&bookId="+str(book_id)
            yield scrapy.Request(book_chapter_number_url,self.parse_book_chapter_number) 
        
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
    
    #作品讨论数 
    def parse_book_threadList(self,response):
        #line 命令行测试
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        
        json_body = json.loads(response.body)
        bookDetailInfo = BookDetailInfo()
        bookDetailInfo['book_discuss_number'] = json_body.get("data").get("threadCnt")
        bookDetailInfo['book_id'] = response.url[47:].split("&")[2][7:]
        
        yield bookDetailInfo
    #章节数
    def parse_book_chapter_number(self,response):
        json_body = json.loads(response.body)
        bookDetailInfo = BookDetailInfo()
        bookDetailInfo['book_chapter_number'] = json_body.get("data").get("chapterTotalCnt")
        bookDetailInfo['book_id'] = response.url.split("&")[1][7:]
        yield bookDetailInfo
        
import pymysql.cursors
#作者信息爬虫
class BookAuthorSpider(scrapy.Spider):
    name = "bookAuthorSpider"
    #db连接
    connection = None
    #私有配置项
    custom_settings = {
        'LOG_FILE': 'scrapy.log',
        'LOG_STDOUT':True
        }
    start_urls = None
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
    #db初始化
    def connect_mysql_db(self):
        self.connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 db='local',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
        
        
    #起始requests
    def start_requests(self):
        #初始化连接db
        self.connect_mysql_db()
        #获取db操作
        cursor = self.connection.cursor()
        sql = """
           select distinct(book_author_url) from qidian_book_detail_info
        """
        cursor.execute(sql)
        #获取所有结果
        results = cursor.fetchall()
        self.connection.close()
        if results:
            for row in results:
                yield scrapy.Request(row['book_author_url'],
                        self.pares_detail_author
                       )

    #爬取作者信息
    def pares_detail_author(self,response):
        bookAuthor = BookAuthor()
        #基础url
        base_author_url = "https://my.qidian.com"
        
        #作者
        bookAuthor['book_author'] = response.xpath("//div[@class='header-msg']//h3//text()").extract_first()
       
        datas = response.xpath("//div[@class='header-msg-data']//span[contains(@class,'mr12')]//strong//text()").extract()
        #作品数量
        bookAuthor['book_author_books'] = datas[0]
        #总创作字数
        bookAuthor['book_author_write_num'] = datas[1]
        #总创作天数
        bookAuthor['book_author_write_days'] = datas[2]
        #作者id
        bookAuthor['book_author_id'] = response.url[29:]
        
        yield bookAuthor

        author_personal_url = response.xpath("//a[@class='header-msg-tosingle']//@href").extract_first()
        if author_personal_url:
            #拼接url
            author_personal_url = base_author_url + author_personal_url 
            
            yield scrapy.Request(author_personal_url,
                        self.pares_author_personal
                      )
    
    #爬取个人页面
    def pares_author_personal(self,response): 
        bookAuthor = BookAuthor()
        infoData = response.xpath("//div[@class='header-msg-desc']//text()").extract_first()
        
        bookAuthor['book_author_id'] = response.xpath("//a[@class='qdp-button-a mlr4']//@href").extract_first()[8:]

        
        if infoData[0] == "男" or infoData[0] == "女":
            #地址
            bookAuthor['book_author_address'] = infoData[4:]
            bookAuthor['book_author_sex'] = infoData[0]
        else:
            bookAuthor['book_author_address'] = infoData[3:]
            
        bookAuthor['book_author'] = response.xpath("//h3[@id='elUidWrap']//a//text()").extract_first()
        
        yield bookAuthor

#读者信息爬虫
class bookReaderSpider(scrapy.Spider):
    name = "bookReaderSpider" 
    book_reader_info_url = "https://my.qidian.com/user/"
    book_reader_num = 100
    
    vip_level = {"icon-gv":"高级VIP",
                 "icon-hy":"高级会员",
                 "icon-cv":"初级VIP",
                 "icon-pt":"普通会员"
                 }
    
    #私有配置项
    custom_settings = {
        'LOG_FILE': 'scrapy.log',
        'LOG_STDOUT':True
        }
    start_urls = None
    #lua脚本
    script = """
           function main(splash, args)
              splash.images_enabled = false
              assert(splash:go(args.url))
              assert(splash:wait(5))
              return {
                html = splash:html(),
              }
        end
    """
    #起始requests
    def start_requests(self):
        #读取 读者信息
        for i in range(self.book_reader_num):
           
            #起步url请求 调用splash 渲染js
            yield  scrapy.Request(self.book_reader_info_url + str(i),
                        self.parse_book_reader
                       )
            
    #抓取读者页面信息
    def parse_book_reader(self,response):
        
        bookRead = BookRead()
        #读者id
        bookRead['book_reader_id'] = response.xpath("//h3[@id='elUidWrap']//@data-id").extract_first()
        #无效链接不操作
        if bookRead['book_reader_id'] == None:
            return 
        
        infoData = response.xpath("//div[@class='header-msg-desc']//text()").extract_first()
        
        if infoData[0] == "男" or infoData[0] == "女":
            #地址
            bookRead['book_reader_address'] = infoData[4:]
            bookRead['book_reader_sex'] = infoData[0]
        else:
            bookRead['book_reader_address'] = infoData[3:]
            bookRead['book_reader_sex'] = "默认"
        #读者名称
        bookRead['book_reader_name'] = response.xpath("//h3[@id='elUidWrap']//a//text()").extract_first()
       
        header_msg_strong = response.xpath("//strong[@class='header-msg-strong']//text()").extract()
        #关注
        bookRead['book_reader_focus'] = header_msg_strong[0]
        #粉丝
        bookRead['book_reader_fans'] = header_msg_strong[1]
        
        #VIP等级       
        vip_key = response.xpath("//div[@class='header-avatar']//a[contains(@class,'icon')]/@class").extract_first()[23:]
        bookRead['book_reader_vip_level'] =  self.vip_level.get(vip_key) 
        if bookRead['book_reader_vip_level'] == None :
            bookRead['book_reader_vip_level'] = "免费用户" 
        #经验等级
        bookRead['book_reader_experience_level'] = response.xpath("//h3[@id='elUidWrap']//a[@class='header-msg-level']//text()").extract_first()[2:]

        yield bookRead
        
        #动态历史数据    
        yield  scrapy.Request("https://my.qidian.com/ajax/User/FriendHistory?id="+bookRead['book_reader_id'],
                        self.parse_reader_history
                      )   
        #粉丝勋章列表
        yield  scrapy.Request("https://my.qidian.com/ajax/User/FriendFansCnt?id="+bookRead['book_reader_id'],
                        self.parse_reader_fansList_list
                      ) 
     
        """
        fans_levels = response.xpath("//ul[@id='fansHonorTab']//a[contains(@class,'elCanTab')]//@data-index").extract()
        
        for i in fans_levels:
            
            yield  scrapy.Request("https://my.qidian.com/ajax/user/FriendFansList?id="+str(bookRead["book_reader_id"])+"&levelId="+str(i),
                        self.parse_reader_fansList,
                      )
        """
    #粉丝勋章列表
    def parse_reader_fansList_list(self,response):
        json_body = json.loads(response.body).get("data").get("config")
        
        book_reader_id = response.url[49:]
        for config in json_body:
            
            yield  scrapy.Request("https://my.qidian.com/ajax/user/FriendFansList?id="+str(book_reader_id)+"&levelId="+str(config.get("levelId")),
                        self.parse_reader_fansList,
                      )

    
    #动态历史数据 json
    def parse_reader_history(self,response):
        bookRead = BookRead()
        
        json_body = json.loads(response.body).get("data").get("historyData")
        
        bookRead['book_reader_id'] = response.url[49:]
        #书架收藏
        bookRead['book_reader_collection_number'] = json_body.get("bshelfCnt")
        #订阅数
        bookRead['book_reader_subscribe_number'] = json_body.get("subscribeCnt")
        #打赏数
        bookRead['book_reader_exceptional_number'] = json_body.get("donateCnt")
        #投月票
        bookRead['book_reader_monthly_ticket_number'] = json_body.get("monthTicketCnt")
        #投推荐票数
        bookRead['book_reader_recommend_number'] = json_body.get("rcmTicketCnt")
        
        yield bookRead
     
    
    #作品
    def parse_reader_fansList(self,response):
        json_body = json.loads(response.body)
        
        #line 命令行测试
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)

        bookReaderPayDetail = BookReaderPayDetail()
        #读者id
        params = response.url[50:].split('&',1)
        bookReaderPayDetail['book_reader_id'] = params[0]
        #粉丝等级
        bookReaderPayDetail['book_reader_fans_level'] = params[1][8:]
        
        
        if json_body.get("data").get('books'):
            for book in json_body.get("data").get('books'):
                #作品id
                bookReaderPayDetail['book_id'] = book.get("bookId")
                #作品名称
                bookReaderPayDetail['book_name'] = book.get("bookName")
                yield bookReaderPayDetail
       
"""

#190001809 
#起点目前 注册用户数  314698589
fetch("https://my.qidian.com/user/190001809")
response.xpath("//title")
url = "https://my.qidian.com/user/"

#粉丝勋章
https://my.qidian.com/ajax/user/FriendFansList?id=190001809&levelId=3
#粉丝勋章列表
https://my.qidian.com/ajax/user/FriendFansCnt?id=190001809
#动态历史数据
https://my.qidian.com/ajax/User/FriendHistory?id=190001809
#讨论数
https://book.qidian.com/ajax/book/GetBookForum?_csrfToken=Iwt2avhIzBnATeNl2WrxCAl0VM5ibH6clhkng5iy&authorId=2432247&bookId=3073025&chanId=12&pageSize=0
#章节数
https://book.qidian.com/ajax/book/category?_csrfToken=Iwt2avhIzBnATeNl2WrxCAl0VM5ibH6clhkng5iy&bookId=1003354631


"""
    