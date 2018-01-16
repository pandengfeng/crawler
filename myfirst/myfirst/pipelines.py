# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html+

#from scrapy.exceptions import DropItem
import json
class MyfirstPipeline(object):
    def process_item(self, item, spider):
        return item

class BdtbPipeline(object):
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
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='123456',
                                 db='local',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    
    def process_item(self, item,spider):
        self.insert_into_table(self.connection,item)
        return item
    
    def insert_into_table(self,conn,item):
        try:
            with conn.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `bdtb_item` (`title`, `message`,`url`,`image`,`userNum`,`postNum`) VALUES (%s, %s, %s, %s, %s, %s)"
                res=cursor.execute(sql, (
                    item['title'],
                    item['message'],
                    item['url'],
                    item['image'],
                    item['userNum'],
                    item['postNum'])
                )
                print(res)
        except (RuntimeError, TypeError, NameError):
            conn.rollback()
    def close_spider(self, spider):
        self.connection.commit()
        self.connection.close()    
