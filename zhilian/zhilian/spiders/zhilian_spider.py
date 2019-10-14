import scrapy

from .. import items
'''
为了可以直接使用scrapy内置的爬虫操作，让scrapy自动采集数据，我们需要定义一个爬虫处理类
在spiders/zhilianspider.py模块中定义ZhilianSpider类型,继承自scrapy.Spider
类型中的属性：name属性~爬虫名称，用于在命令行启动爬虫时调用
类型中的属性：start_urls属性~采集数据的初始url地址[列表、元组]
类型中的属性：allowed_domains属性~采集数据的网站域名限制
类型中的方法：parse(self, response)采集完数据之后自动执行的函数

'''
class ZhilianSpider(scrapy.Spider):
    name = 'zlspider'
    #todo： 项目运行命令：python3 -m scrapy crawl zlspider

    # 起始url
    start_url = ['https://sou.zhaopin.com/?jl=%E9%83%91%E5%B7%9E&kw=Python&kt=3&sf=0&st=0']
    # 域名限制
    allowed_domains=['zhaopin.com']

    # 重写parse函数
    def parse(self, response):
        '''
        在这里，从下载模块获取的数据response不在此函数中处理，这个函数只是将获取的第一个url
        加入到urljoin（）中管理，暂时不做数据处理
        并将scrapy.Request()请求对象提交到parse_response()函数中，此时后面若提交了与此url相同改的
        url，则urljoin（）会自动去重

        :param response:
        :return:
        '''
        # 将url加入到urljoin中
        url = response.urljoin(self.start_url[0])
        # 将请求数据交给self.parse_response()进行处理
        yield scrapy.Request(url,callback=self.parse_response)

    def parse_response(self,response):
        # 采集到的数据就在response中，定义专门保存items对象即数据对象的列表
        job_items = []
        # xpath语法，先筛选出智联招聘每一条招聘信息，即每一行
        job_list = response.xpath('//*[@id="listContent"]/div')

        for job in job_list:
            job_name = job.xpath('//*[@id="listContent"]/div[1]/div/a/div[1]/div[1]/span')
            company_name = job.xpath('//*[@id="listContent"]/div[1]/div/a/div[1]/div[2]')
            salary = job.xpath('//*[@id="listContent"]/div[1]/div/a/div[2]/div[1]/p')
            # 实例化items对象
            job_item = items.ZhilianItem()
            job_item['job_name']=job_name
            job_item['company_name']=company_name
            job_item['salary']=salary
            job_items.append(job_item)
            # todo：这个方法是将 数据保存在本地文件中
            # 将列表返回，通过python3 -m scrapy crawl zlspider -o job.csv
            # 可以将数据保存在名为job的.csv文件，即表格文件汇总，文件的后缀名可选的有csv/json/jl/jsonline等
            # return job_times
            # 将数据交给Pipelines模块
            yield job_item


        # next_page,在当前路由页面中获取下一页的链接，得到后面所有页面的链接列表
        # 该列表中包含了第一个url，由于第一个url也已经交由urljoin（）管理，所以若后面urljoin（）再次遇到相同的rul
        # 就会自动去重，类似python中的集合set

        next_list = response.xpath('//*[@id="pagination_content"]/div').extract()

        for page in next_list:
            # 将链接加入到urljoin列表中
            url = response.urljoin(page)

            # 将请求数据交给self.parse()进行处理，递归获取数据的筛选，并通过yield job_item
            # 将数据提交给管道模块进行保存
            yield scrapy.Request(url,callback=self.parse_response)


        '''
        关于深度获取：
        在获取到智联招聘第一页的url后，可以通过response.xpath()对该页面上存在的第2、3、4、5....的链接href进行获取。先获取
        第一个页面，进行相应的字段筛选，构建item数据类型并交给pipeline模块进行保存到数据库，依次循环。为了保证获取到的
        链接不会与第一个页面的url重复，我们在parse()函数中并没有直接对第一页数据进行筛选和提交，而是把url交给了
        response.urljoin()进行管理，并且创建srapy.Request(url,callback=self.parse_response)请求对象，并将其交给parse_response
        （）函数进行处理，也就是将第一页爬取到的数据交给parse_response（）进行数据处理，在
        parse_response（）函数中，首先处理了第一页的数据，并从中筛选出了所有的页面链接，包括了其他页面，同时也包括了
        原来的第一页，每个url都要交个response.urljoin()进行管理，当urljoin（）遇到了重复的url，会自动去重，所以这样就获取到
        了完整的并且不会重复的数据。如果筛选的条件不同，导致总的页数不一样，也可以通过这种方法进行深度爬取，获取到完整的
        数据。

'''

