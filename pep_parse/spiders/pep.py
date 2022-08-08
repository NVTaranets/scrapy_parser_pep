import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        table_index_pep = response.css('section[id=numerical-index] tbody')
        peps = table_index_pep.css('tr')
        for pep_link in peps.css('a::attr(href)'):
            # Возвращаем response.follow() с вызовом метода parse_author()
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        name = response.css('h1.page-title::text').get()
        data = {
            'number': name.split()[1],
            'name': name,
            'status': response.css('dt:contains("Status") + dd::text').get()
        }
        yield PepParseItem(data)
