import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
    ]

    custom_settings = {
        'FEEDS':{
        'quotes.json':{
        'format':'json',
        'encoding':'utf8',
        
        }
        },
    }

    def parse_only_quotes(self, response, **kwargs):
        if kwargs:
            quotes = kwargs['quotes']
        quotes.extend(response.xpath(
            '//span[@class="text" and @itemprop="text"]/text()').getall())
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs = {'quotes': quotes})
        else: 
            yield{
                'quotes': quotes
            }
    def parse (self, response):

        print('\n\n')

        title = response.xpath('//h1/a/text()').get()

        quotes = response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall()

        top_tags = response.xpath('//div[contains(@class, "tags-box")]//span[@class="tag-item"]/a/text()').getall()

        top = getattr(self, 'top', None)
        if top: 
            top = int(top)
            top_tags = top_tags[:top]
        yield {
            'title': title,
            'top_tags': top_tags
        }

        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        if next_page_button_link:
            yield response.follow(next_page_button_link, callback=self.parse_only_quotes, cb_kwargs = {'quotes': quotes})
