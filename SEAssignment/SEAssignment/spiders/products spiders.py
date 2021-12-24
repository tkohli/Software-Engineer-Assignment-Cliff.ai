import scrapy


class QuotesSpider(scrapy.Spider):
    name = "products"

    def start_requests(self):
        urls = [
            'https://www.net-a-porter.com/en-in/shop/clothing/tops?pageNumber=1'
        ]
        for i in range(2, 27):
            urls.append(
                "https://www.net-a-porter.com/en-in/shop/clothing/tops?pageNumber="+str(i))
        for i in range(1, 27):
            urls.append(
                "https://www.net-a-porter.com/en-in/shop/shoes?pageNumber="+str(i))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # title = response.css('title::text').get()
        # yield {'title': title}
        # for quote in range(50):
        # items['Titles'] = title
        for quote in response.css('div.ProductItem24__p'):
            category = response.css(".FilterTags52__tag::text").get()
            if category == "Tops":
                category = 'Topwear'
            else:
                category = 'Footwear'
            yield {
                'name': quote.css('.ProductItem24__designer::text').get(),
                'brand': quote.css('.ProductItem24__name::text').get(),
                'price': float(quote.css('span::text')[2].get()[1:].replace(',', '')),
                'sale_price':float(quote.css('span::text')[2].get()[1:].replace(',', '')),
                'image_url': quote.css('img').xpath('@src').get(),
                'product_page_url': response.css('.ProductGrid52 a::attr(href)').get(),
                'product_category': category
            }
