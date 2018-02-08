# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#import logging
import json
from qidianSpider.items import BookDetailInfo
from qidianSpider.items import BookTags
from qidianSpider.items import BookAuthor
#import sys
class QidianspiderPipeline(object):
    def __init__(self):
        self.file = open('data.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        if isinstance(item, BookAuthor):
            try:
                line = json.dumps(dict(item), ensure_ascii=False) + "\n"
                self.file.write(line)
            except Exception:
                pass
     
        return item
    def open_spider(self, spider):
        pass
    def close_spider(self, spider):
        pass

import pymysql.cursors

class MySQLStorePipeline(object):
    #db连接
    connection = None

    def __init__(self):
        #self.file = open('data.json', 'w', encoding='utf-8')
        self.connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 db='local',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    def process_item(self, item,spider):
        
        if isinstance(item, BookDetailInfo):
            try:
                self.insert_into_table_BookDetailInfo(item)
            except Exception:
                pass
            
        if isinstance(item, BookTags):
            try:
                self.insert_into_table_BookTags(item)
            except Exception:
                pass   
            
        if isinstance(item, BookAuthor):
            try:
                self.insert_into_table_BookAuthor(item)
            except Exception:
                pass 
          
        return item
    
    
    def insert_into_table_BookDetailInfo(self,item):

            with self.connection.cursor() as cursor:
                # Create a new record
                sql = """
                    INSERT INTO `qidian_book_detail_info`
                    (book_id,book_name,book_author,book_author_url,book_words_number
                    ,book_click_quantity,book_recommend_number,book_monthly_ticket_number,book_support_number
                    ,book_introduction,book_chapter_number,book_discuss_number,book_near_update_time,book_page_url) 
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   """
                cursor.execute(sql, (
                    item['book_id'],item['book_name'],item['book_author'],item['book_author_url'],item['book_words_number']
                    ,item['book_click_quantity'],item['book_recommend_number']
                    ,item['book_monthly_ticket_number']
                    ,item['book_support_number']
                    ,item['book_introduction']
                    ,item['book_chapter_number']
                    ,item['book_discuss_number']
                    ,item['book_near_update_time']
                    ,item['book_page_url']
                ))

    def insert_into_table_BookTags(self,item):
        
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `qidian_book_tags` (`book_id`, `book_tag`) VALUES (%s, %s)"
                cursor.execute(sql, (
                    item['book_id'],
                    item['book_tag'])
                )
        except (RuntimeError, TypeError, NameError):
            self.connection.rollback()
           
    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()
        
    
    
    def insert_into_table_BookAuthor(self,item):
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                if item['book_author_books'] != "默认":
                    sql ="""INSERT INTO qidian_book_author (book_author_id,book_author, book_author_sex
                    ,book_author_books,book_author_write_num,book_author_write_days,book_author_address) 
                    VALUES (%s,%s, %s,%s, %s,%s, %s)
                    """
                    cursor.execute(sql, (
                        item['book_author_id'],
                        item['book_author'],
                        item['book_author_sex'],
                        item['book_author_books'],
                        item['book_author_write_num'],
                        item['book_author_write_days'],
                        item['book_author_address'])
                        )
                else:
                    sql = """update qidian_book_author set 
                        book_author_address = %s , book_author_sex = %s
                        where book_author_id = %s
                    """
                    cursor.execute(sql, (
                        item['book_author_address'],
                        item['book_author_sex'],
                        item['book_author_id'])
                        )
        except (RuntimeError, TypeError, NameError):
            self.connection.rollback()