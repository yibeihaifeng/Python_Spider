# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ZhilianPipeline(object):
    def process_item(self, item, spider):
        return item

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 替换mysqldb模块
import pymysql

pymysql.install_as_MySQLdb()

# 在Pipeline.py文件中  定义用于接收并保存数据到Mysql数据库的类型


class ZhilianPileline(object):
    '''
    定义__init__函数，用户初始化数据，可用于打开文件，打开数据库连接等
    构造函数，在类被实例化之后自动调用的函数
    '''

    def __init__(self):
        self.engine = create_engine('postgresql://admin:admin@localhost/python_spider?charst=utf8')
        # 创建会话构建对象
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def open_spider(self,spider):
        '''
        爬虫开启时需要调用的函数，经常用户数据初始化
        :param spider:
        :return:
        '''
        pass



    def close_spider(self,spider):
        '''
        爬虫程序关闭时自动调用的函数，经常用于做一些资源回收的工作，
        如关闭和数据库的会话连接
        :param spider:
        :return:
        '''
        self.session.close()



    def process_item(self,item,spider):
        '''
        核心处理模块，该函数会接受爬虫程序已经封装好的item对象，
        通过sql语句，将数据存储在数据库中
        :param item:
        :param spider:
        :return:
        '''
        print('正在保存数据到数据库中...')
        sql = "insert into job(job_name,company_name,salary) values('%s','%s','%s')"%(item['job_name'],item['company'],item['salary'])
        # 执行sql语句
        self.session.execute(sql)
        self.session.commit()