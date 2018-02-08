# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

"""
create table qidian_book_detail_info(
    book_id VARCHAR(128) not null PRIMARY  KEY COMMENT '作品id',
    book_name VARCHAR(128) COMMENT '作品名称',
    book_author VARCHAR(128) COMMENT '作者',
    book_author_url VARCHAR(128) COMMENT '作者页面url',
    book_words_number VARCHAR(128)COMMENT '字数',
    book_click_quantity VARCHAR(128) COMMENT '点击量',
    book_recommend_number VARCHAR(128) COMMENT '推荐数',
    book_monthly_ticket_number VARCHAR(128) COMMENT '月票数',
    book_support_number VARCHAR(128) COMMENT '打赏数',
    book_introduction text COMMENT '简介',
    book_chapter_number VARCHAR(128) COMMENT '章节数',
    book_discuss_number VARCHAR(128) COMMENT '讨论数',
    book_near_update_time VARCHAR(128) COMMENT '最近更新时间',
    book_page_url VARCHAR(128) COMMENT '作品页面链接'
);

"""
#作品详情
class BookDetailInfo(scrapy.Item):
    #作品id
    book_id = scrapy.Field()
    #作品名称
    book_name = scrapy.Field()
    #作者
    book_author = scrapy.Field()
    #作者链接
    book_author_url = scrapy.Field()
    #字数
    book_words_number = scrapy.Field()
    #点击量
    book_click_quantity = scrapy.Field()
    #推荐数
    book_recommend_number = scrapy.Field()
    #月票数
    book_monthly_ticket_number = scrapy.Field()
    #打赏数
    book_support_number = scrapy.Field()
    #简介
    book_introduction = scrapy.Field()
    #章节数
    book_chapter_number = scrapy.Field()
    #讨论数
    book_discuss_number = scrapy.Field()
    #最近更新时间
    book_near_update_time = scrapy.Field()
    #作品页面链接
    book_page_url = scrapy.Field()


"""
create table qidian_book_tags(
    book_id VARCHAR(128) not null COMMENT '作品id',
    book_tag VARCHAR(128) not null COMMENT '标签' 
);

"""  
#作品对应标签
class BookTags(scrapy.Item):
    #作品id
    book_id = scrapy.Field()
    #标签
    book_tag = scrapy.Field()
    
""" 
create table qidian_book_author(
    book_author_id VARCHAR(128) not null PRIMARY  KEY COMMENT '作者',
    book_author VARCHAR(128) ,
    book_author_sex VARCHAR(128) COMMENT '性别',
    book_author_books VARCHAR(128) COMMENT '作品数量',
    book_author_write_num VARCHAR(128) COMMENT '总创作字数',
    book_author_write_days VARCHAR(128) COMMENT '总创作天数',
    book_author_address VARCHAR(128) COMMENT '地址'
)
""" 

class BookAuthor(scrapy.Item):
    #作者编号
    book_author_id = scrapy.Field()
    #作者
    book_author = scrapy.Field()
    #性别
    book_author_sex = scrapy.Field()
    #作品数量
    book_author_books = scrapy.Field()
    #总创作字数
    book_author_write_num = scrapy.Field()
    #总创作天数
    book_author_write_days = scrapy.Field()
    #地址
    book_author_address = scrapy.Field()