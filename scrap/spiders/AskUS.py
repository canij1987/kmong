from __future__ import unicode_literals
from bs4 import BeautifulSoup
import scrapy
import json

class AskUSSpider(scrapy.Spider):
    name = 'AskUS_visa_links'
    base_url = 'http://ask.koreadaily.com/ask/'
    start_page = 1
    end_page = 282
    start_urls = ['http://ask.koreadaily.com/ask/ask_list.asp?page=%s&searchOpt=&searchTxt=&branch=&qca_code=visa.visa&cot_userid=&status=' % i for i in range(start_page, end_page + 1)]

    def parse(self, response):
        selects = response.xpath('//table[@id="notice"]//tr[@class="general-question"]')
        #nums = selects.xpath('td[2]/text()').extract()
        #subjects = selects.xpath('td[4]/a/text()')
        links = selects.xpath('td[4]/a/@href').extract()
        for link in links:
            url = self.base_url + link
            yield {'link':url} 


class AskUSVISASpider(scrapy.Spider):
    name = 'AskUS_visa'
    s_url = [] 
    json_data = open('v_links.json').read()
    data = json.loads(json_data)
    for datum in data:
        s_url += [datum['link']]
    start_urls = s_url 

    def parse(self, response):
        selects = response.xpath('//td[@id="frame_center"]/table/tr[1]/td/div')
        title = selects.xpath('//h1/text()').extract_first()
        view = selects.xpath('//p/text()')[2].extract()
        author = selects.xpath('//p/text()')[3].extract()
        location = selects.xpath('//strong/script/text()').extract_first()[12:14]
        date = selects.xpath('//p/font/text()')[1].extract()[4:]
        content = BeautifulSoup(selects.xpath('//td/font')[0].extract(), 'lxml').text.strip()
        soup = BeautifulSoup(selects.xpath('//td/font')[2].extract(), 'lxml')
        reply = soup.text.strip()
        professor = BeautifulSoup(selects.xpath('//td/font')[1].extract(), 'lxml').text.strip()
        yield {'제목':title,
                '조회':view,
                '작성자': author,
                '지역': location,
                '작성시간': date,
                '내용': content,
                '전문가': professor,
                '답변': reply
                }
