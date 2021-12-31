import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'items'

    def start_requests(self):
        urls = [
            'https://www.net-a-porter.com/en-in/shop/clothing/tops?pageNumber=1'
        ]
        for i in range(2, 27):
            urls.append(
                'https://www.net-a-porter.com/en-in/shop/clothing/tops?pageNumber='+str(i))
        for i in range(1, 35):
            urls.append(
                'https://www.net-a-porter.com/en-in/shop/shoes?pageNumber='+str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for data in response.css('div.ProductItem24__p'):
            ext_price = data.css('.PriceWithSchema9__value span::text').get()
            price = ''
            for p in ext_price:
                if p != '$' and p != ',':
                    price += p
            price = float(price)
            image = data.css('.secondaryImage img').xpath(
                '@src').extract_first()
            if image is None:
                image = data.xpath('//img/@src').extract_first()
            category = response.css(".FilterTags52__tag::text").get()
            if category == "Tops":
                category = 'Topwear'
            else:
                category = 'Footwear'
            yield {
                'Name': data.css('.ProductItem24__designer::text').get(),
                'brand': data.css('.ProductItem24__name::text').get(),
                'original_price': price,
                'sale_price': price,
                'image_url': image,
                'product_page_url': data.css('meta').xpath('@content').extract_first(),
                'product_category': category,
            }
