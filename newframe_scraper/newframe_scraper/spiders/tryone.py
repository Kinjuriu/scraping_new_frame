import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from newframe_scraper.items import NewsArticle
from lxml import etree

def generate_start_urls():
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    return ['https://www.newframe.com/image-sitemap-{}.xml'.format(number) for number in numbers]

class TryOneSpider(scrapy.Spider):
    name = 'newFrame'
    allowed_domains = ['newframe.com']
    start_urls = ['https://www.newframe.com/image-sitemap-2.xml'] #generate_start_urls()
    
    
    def parse(self, response):
        print("----bef----")
        
        content = response.xpath("//url").get()
        print(content)
        print("kkkkkkkkkkkkkkk")
        print('parse_article url:', response.url)
        sitemap = etree.fromstring(response.body)
        for child in sitemap.getchildren():
            inner_children = child.getchildren()
            news_child = [x for x in inner_children if 'news' in x.tag]
            if not news_child:
                continue
            else:
                news_child = news_child[0]
                stock_child = [x for x in news_child if 'stock_tickers' in x.tag]
                keywords_child = [x for x in news_child if 'keywords' in x.tag]
                title_child = [x for x in news_child if 'title' in x.tag]
                if stock_child:
                    yield {
                        'stock_tickers': stock_child[0].text,
                        'keywords': keywords_child[0].text,
                        'title': title_child[0].text,
                    }
