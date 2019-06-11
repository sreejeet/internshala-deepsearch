# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime
from ..items import InternshalaItem

class DeepsearchSpider(scrapy.Spider):
    """ Internshala throttles requests, so there is a 0.5 second delay
    on each request. Fell free to modify it as per your requirements.
    ../settings.py : DOWNLOAD_DELAY

    You can reduce the number of internships to search by providing
    search keyword directly to uinternshala before running this custom search 
    start_urls = ['https://internshala.com/internships/keywords-python']

    As usual, the user is responsible for ethical use of this or
    any software and the author shall not be liable in any manner.
    """
    
    name = 'DeepSearch'
    allowed_domains = ['internshala.com']
    start_urls = ['https://internshala.com/internships/']


    # Internships must contain these keywords 
    keywords = []

    # Internships must contain at least one these keywords 
    keywords_any_one = ['from home', 'delhi', 'noida']


    def parse(self, response):

        # Go to details page of each internship
        for link in response.css('.view_detail_button::attr("href")'):
            request = response.follow(response.urljoin(link.extract()), callback=self.parse_job)
            yield request

        # Link for next page
        nextUrl = response.css('#navigation-forward::attr("href")').extract_first()
        yield scrapy.Request(url=response.urljoin(nextUrl))


    def parse_job(self, response):

        details_text = response.css('.internship_list_container').extract_first().lower()

        # Must keywords
        if self.keywords:
            for keyword in self.keywords:
                if not keyword.lower() in details_text:
                    print('%s not found. Skipping.' % keyword)
                    return

        # Any one keywords
        if self.keywords_any_one:
            none = True
            for keyword in self.keywords_any_one:
                if keyword.lower() in details_text:
                    none = False
                    break

            if none:
                print('Skipping')
                return

        # Create and yeild InternshalaItem
        # ../items : InternshalaItem
        item = InternshalaItem()
        item['heading'] = response.css('.profile_on_detail_page::text').extract_first().strip()
        item['recruiter'] = response.css('.link_display_like_text::attr("title")').extract_first().strip()
        item['heading'] = response.css('.profile_on_detail_page::text').extract_first().strip()
        item['start_date'] = response.css('#start-date-first::text').extract_first().strip()
        item['duration'] = response.css('.table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)::text').extract_first().strip()
        item['stipend'] = response.css('.stipend_container_table_cell::text').extract_first().strip()
        item['locations'] = response.css('.location_link::text').extract_first().strip()
        item['posted_on'] = response.css('.table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4)::text').extract_first().strip()
        item['apply_by'] = response.css('.table > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(5)::text').extract_first().strip()

        vacancies = response.css('.number_of_internships_available::text').extract_first()
        item['vacancies_available'] = vacancies.strip() if vacancies else 'Unknown'

        item['scraped_on'] = datetime.ctime(datetime.now())
        item['link'] = response.url

        yield item
