import scrapy

screen_name = 'faridebrahimi62'
status_id = '1117417835838550018'


class BrickSetSpider(scrapy.Spider):
    name = 'brick_spider'
    start_urls = ['https://twitter.com/' + screen_name + '/status/' + status_id + '/retweets']

    def parse(self, response):
        print(response)
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            NAME_SELECTOR = 'h1 ::text'
            PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            IMAGE_SELECTOR = 'img ::attr(src)'
            yield {
                'name': brickset.css(NAME_SELECTOR).extract_first(),
                'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
                'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
                'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            }

        NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
