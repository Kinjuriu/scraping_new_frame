from turtle import title
import scrapy
import pandas as pd
from lxml.etree import XMLSyntaxError




class NewframeSpider(scrapy.Spider):
    name = 'newframe'
    allowed_domains = ['newframe.com']
    # start_urls = ['https://www.newframe.com/resilience-persists-cape-towns-marikana/']

    def extract_urls(sitemap, index=True):
        urls = pd.DataFrame()
        if index:
            sitemap_index_df = pd.read_xml(sitemap)
            for xml_sitemap in sitemap_index_df['loc'].tolist():
                try:
                    urls = pd.concat([urls, pd.read_xml(xml_sitemap)])
                except XMLSyntaxError:
                    print(xml_sitemap, 'unreadable.')
                except UnicodeEncodeError:
                    print(xml_sitemap, 'unicode error.')
        else:
            urls = pd.read_xml(sitemap)
        return urls


    wordpress = extract_urls('https://www.newframe.com/image-sitemap-1.xml', index=False)
    print("****pre****")
    wordpress.head()
    print(wordpress['loc'])
    print("****after****")
    myFunkyList = wordpress['loc']
    start_urls = wordpress['loc'].values.tolist()
    def parse(self, response):
        #title = response.css('span.title::text').get()
        title = response.xpath('//h1[@class="post-title"]/text()').get()
        author = response.xpath('//a[@class="text"]/text()').get()
        date = response.xpath('//span[@class="the-date"]/text()').get()
        # //div[@class="medium-8 columns"]/p[following-sibling::p/strong]/text()
        # content = response.xpath('//p/text()').get()
        # content = response.xpath('//article[@class="post-content"]/p/*').get()
        # /p[normalize-space()]
        content = response.xpath('//article[@class="post-content"]//p').get()
        
        return {"title": title, "author":author, "date": date, "content": content}

