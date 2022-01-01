from urllib import parse
import scrapy

# Use crawler process to run scrapy from within the a python script
from scrapy.crawler import CrawlerProcess
import json



class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.bbc.com']
    start_urls = ['https://www.bbc.com//']

    with open('newslinks.json','w') as f:
        f.write(' ')
    def parse(self, response):

        link = response.css("h3.media__title a::attr(href)").getall()

        for i in range(len(link)):
            if link[i][:4] != 'http':
                link[i] = 'https://www.bbc.com'+ link[i]
            else:
                pass
        title = response.css("h3.media__title a::text").getall()

        for i in range(len(title)):
            title[i] = title[i].strip()
        
        heading = response.css("h3.media__title a::attr(rev)").getall()

        for i in range(len(heading)):
            heading[i] = heading[i].split('|')[0]

        news = {}
        news['link'] = link
        news['title'] = title
        news['heading'] = heading

        with open('newslinks.json','a') as f:
            f.write(json.dumps(news, indent=2)+'\n')


# main driver

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(NewsSpider)
    process.start()