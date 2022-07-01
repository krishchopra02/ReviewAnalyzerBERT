import re
import pandas as pd
import scrapy 

class Pages(scrapy.Spider):
    name = "Review_Sentiment"
    company_data  = pd.read_csv('../../URL_extraction/data/company_urls.csv')
    start_urls = company_data['urls'].unique().tolist()

    def parse(self,response):

        company_name = response.xpath("//span[contains(@class,'typography_h1__Xmcta')]/text()").extract_first()
        company_web = response.xpath('//a[@target="_blank"]/@href').extract_first()
        company_logo = response.xpath('//img[contains(@class,"business-profile-image_image__jCBDc")]/@src').extract_first()
        reviews= response.xpath('//p[@data-service-review-text-typography="true"]')
        reviews = [review.xpath('.//text()').extract() for review in reviews]
        reviews = [[r.strip() for r in review] for review in reviews]
        reviews = [' '.join(review) for review in reviews]
        ratings = response.xpath('//div[contains(@class,"styles_reviewHeader__iU9Px")]//@data-service-review-rating').extract()
        print(ratings)
        ratings = [int(re.match('\d+',rating).group(0)) for rating in ratings]
        for review,rating in zip(reviews,ratings):
            yield {
                'review':review,
                'rating':rating,
                'url_website':response.url,
                'company_name':company_name,
                'company_website':company_web,
                'comapny_logo':company_logo
            }
        next_page = response.css('a[data-pagination-button-next-link] ::attr(href)').extract_first()
        if next_page is not None:
            request = response.follow(next_page,callback=self.parse)
            yield request

