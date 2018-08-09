# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Request
from steam.items import SteamItem


class SteampoweredSpider(scrapy.Spider):
    name = "steampowered"
    allowed_domains = ["steampowered.com"]
    start_urls = ['http://store.steampowered.com/search/?term=']
    cookie = {'steamLogin': '',
              'birthtime': '706032001',
              'lastagecheckage': '17-May-1992',
              'mature_content': '1'}

    def parse(self, response):
        urls = response.xpath('//div[@id="search_result_container"]/div/a/@href').extract()
        next_url = response.xpath('//div[@class="search_pagination_right"]/a[@class="pagebtn"]')
        for url in urls:
            yield Request(url, cookies=self.cookie,
                          callback=self.parse_app)
        for n,value in enumerate(next_url.xpath('text()').extract()):
            if value == '>':
                url = next_url.xpath('@href').extract()[n]
                yield Request(url, callback=self.parse)

    def parse_app(self, response):
        item = SteamItem()
        try:
            name = response.xpath('//div[@class="apphub_AppName"]/text()').extract_first("")
            url = response.xpath("//div[@class='block_content_inner']/div[2]/a/@href").extract_first("")
            tag = response.xpath('//div[@class="block_content_inner"]/div[1]/a/text()').extract()
            review = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[1]/div[2]/span[1]/text()'\
                                    ).extract_first()
            review_num = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[1]/div[2]/span[2]/text()'\
                                        ).extract_first("").strip()
            review_des = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[1]/div[2]/span[3]/text()'\
                                        ).extract_first("")
            all_review = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/span[1]\
            /text()').extract_first()
            all_review_num = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/meta\
            [1]/@content').extract_first()
            all_review_des = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[2]/div[2]/span[3]/text()'\
                                            ).extract_first("")
            release_date = response.xpath("//div[@class='release_date']/div[2]/text()").extract_first("")
            developers = response.xpath('//*[@id="developers_list"]/a/text()').extract_first("")
            distributors = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[3]/div/div[4]/div[2]/a/text()'\
                                          ).extract_first("")
            description = response.xpath('//*[@id="game_area_description"]/text()').extract()
            description_text = ''
            for i in description:
                description_text = description_text + i.strip()
            user_tag = response.xpath('//*[@id="game_highlights"]/div[1]/div/div[4]/div/div[2]/a/text()').extract()
            user_tag_list = []
            for i in user_tag:
                i = i.strip()
                user_tag_list.append(i)
            discount = response.xpath('//div[@class="discount_pct"]/text()').extract_first()
            original_price = response.xpath('//div[@class="discount_original_price"]/text()').extract_first()
            final_price = response.xpath('//div[@class="discount_final_price"]/text()').extract_first()
            price = response.xpath('//div[@class="game_purchase_price price"]/text()').extract_first("").strip()

            item['name'] = name
            item['url'] = url
            item['id'] = response.url
            if tag and tag[:-2]:
                item['tag'] = tag[:-2]
            item['review'] = review
            item['review_num'] = review_num
            review_des_re = re.search('\d*%', review_des)
            if review_des_re is not None:
                item['review_des'] = review_des_re.group()
            item['all_review'] = all_review
            item['all_review_num'] = all_review_num
            all_review_des_re = re.search('\d*%', all_review_des)
            if all_review_des_re is not None:
                item['all_review_des'] = all_review_des_re.group()
            item['release_date'] = release_date
            item['developers'] = developers
            item['distributors'] = distributors
            item['description_text'] = description_text
            item['user_tag'] = user_tag_list
            item['discount'] = discount
            item['original_price'] = original_price
            item['final_price'] = final_price
            item['price'] = price

            item['mac'] = {
                'minumum': {
                    'os':  response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "OS")]/following-sibling::text()'
                    ).extract_first(),
                    'Processor': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Processor")]/following-sibling::text()'
                    ).extract_first(),
                    'Memory': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Memory")]/following-sibling::text()'
                    ).extract_first(),
                    'Graphics': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Graphics")]/following-sibling::text()'
                    ).extract_first(),
                    'DirectX': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "DirectX")]/following-sibling::text()'
                    ).extract_first(),
                    'Storage': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Storage")]/following-sibling::text()'
                    ).extract_first()
                },
                'recommended':{
                    'os':  response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "OS")]/following-sibling::text()'
                    ).extract_first(),
                    'Processor': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Processor")]/following-sibling::text()'
                    ).extract_first(),
                    'Memory': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Memory")]/following-sibling::text()'
                    ).extract_first(),
                    'Graphics': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Graphics")]/following-sibling::text()'
                    ).extract_first(),
                    'DirectX': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "DirectX")]/following-sibling::text()'
                    ).extract_first(),
                    'Storage': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="mac"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Storage")]/following-sibling::text()'
                    ).extract_first()
                }
            }
            item['win'] = {
                'minumum': {
                    'os': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "OS")]/following-sibling::text()'
                    ).extract_first(),
                    'Processor': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Processor")]/following-sibling::text()'
                    ).extract_first(),
                    'Memory': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Memory")]/following-sibling::text()'
                    ).extract_first(),
                    'Graphics': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Graphics")]/following-sibling::text()'
                    ).extract_first(),
                    'DirectX': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "DirectX")]/following-sibling::text()'
                    ).extract_first(),
                    'Storage': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Storage")]/following-sibling::text()'
                    ).extract_first()
                },
                'recommended': {
                    'os': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "OS")]/following-sibling::text()'
                    ).extract_first(),
                    'Processor': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Processor")]/following-sibling::text()'
                    ).extract_first(),
                    'Memory': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Memory")]/following-sibling::text()'
                    ).extract_first(),
                    'Graphics': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Graphics")]/following-sibling::text()'
                    ).extract_first(),
                    'DirectX': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "DirectX")]/following-sibling::text()'
                    ).extract_first(),
                    'Storage': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="win"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Storage")]/following-sibling::text()'
                    ).extract_first(),
                }
            }
            item['linux'] = {
                'minumum': {
                    'os': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "OS")]/following-sibling::text()'
                    ).extract_first(),
                    'Processor': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Processor")]/following-sibling::text()'
                    ).extract_first(),
                    'Memory': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Memory")]/following-sibling::text()'
                    ).extract_first(),
                    'Graphics': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Graphics")]/following-sibling::text()'
                    ).extract_first(),
                    'DirectX': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "DirectX")]/following-sibling::text()'
                    ).extract_first(),
                    'Storage': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Minimum")]/\
                        following-sibling::ul//*[contains(text(), "Storage")]/following-sibling::text()'
                    ).extract_first()
                },
                'recommended': {
                    'os': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "OS")]/following-sibling::text()'
                    ).extract_first(),
                    'Processor': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Processor")]/following-sibling::text()'
                    ).extract_first(),
                    'Memory': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Memory")]/following-sibling::text()'
                    ).extract_first(),
                    'Graphics': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Graphics")]/following-sibling::text()'
                    ).extract_first(),
                    'DirectX': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "DirectX")]/following-sibling::text()'
                    ).extract_first(),
                    'Storage': response.xpath(
                        '//div[@class="sysreq_contents"]/div[@data-os="linux"]//ul/*[contains(text(), "Recommended")]/\
                        following-sibling::ul//*[contains(text(), "Storage")]/following-sibling::text()'
                    ).extract_first()
                }
            }
        except Exception as e:
            pass
        yield item