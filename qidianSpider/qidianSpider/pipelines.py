# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from qidianSpider.items import BookDetailInfo
from qidianSpider.items import BookTags

class QidianspiderPipeline(object):
    def __init__(self):
        self.file = open('data.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
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
            
        return item
    
    
    def insert_into_table_BookDetailInfo(self,item):
        
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                sql = """
                    INSERT INTO `qidian_book_detail_info` 
                    (`book_id`, 
                    `book_name`,
                    `book_author`,
                    `book_words_number`
                    ) VALUES (%s,%s,%s,%s)
                   """
                cursor.execute(sql, (
                    item['book_id'],
                    item['book_name'],
                    item['book_author'],
                    item['book_words_number'])
                )
        except (RuntimeError, TypeError, NameError):
            print()
            self.connection.rollback()
    
    
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
