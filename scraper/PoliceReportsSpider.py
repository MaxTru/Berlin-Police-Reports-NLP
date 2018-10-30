"""A Scrapy Spider class which scrapes the data set for this project. It can be run with Scrapy (i.e. following command:
"<your virtual environment>\Lib\site-packages\scrapy\cmdline.py runspider policeReportsSpider.py -o <output filename>"
(Working directory needs to be <...>\Berlin-Police-Reports-NLP\scraper)
"""

import scrapy

class PoliceReport(scrapy.Item):
    """Scrapy Items which defines the fields of a single scraped Police Report."""
    link = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    event = scrapy.Field()

class PoliceReportsSpider(scrapy.Spider) :

    # identification of the Spider
    name = "police_reports_spider"
    # allowed domains for crawling websites
    allowed_domains = ['berlin.de']
    # the list of archive URLs used to create the initial requests for the Spider
    start_urls = [
       # 'https://www.berlin.de/polizei/polizeimeldungen/archiv/2014/',
       # 'https://www.berlin.de/polizei/polizeimeldungen/archiv/2015/',
        #'https://www.berlin.de/polizei/polizeimeldungen/archiv/2016/',
        #'https://www.berlin.de/polizei/polizeimeldungen/archiv/2017/',
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2018/'
    ]
    BASE_URL = 'https://www.berlin.de'

    def parse(self, response):
        """Method that is called by Scrapy for the given start_urls.

        Returns
        -------
        scrapy.Request
            Returns another call to a page to be scraped (i.e. a request). Two types of requests are possible:
            1. for all Police Reports linked on the archive pages, the individual request is returned. As callback
               the self.parse_report method will be called.
            2. since the archive pages list all reports on several pages, for each next page, a new requests will be
               returned. This request is handled with this method again (self.parse())."""
        # Using the response object of CSS to extract all reports from the crawled URLs
        links = response.css(".list-autoteaser li a").re(r'/polizei.+\.php')
        # Now, for every police report we find, call a separate parse function
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_report)
        # Now, check whether there is another page with more reports, if so call that page and start crawling again
        next_page = response.css('.pager-item-next > a::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_report(selfself, response):
        """Method that is called for each report which was identified on the archive pages."""
        item = PoliceReport()
        item["link"] = response.url
        item["title"] = response.css("h1.title::text").extract()
        item["date"] = response.css(".polizeimeldung::text").re("[0-9]+\.[0-9]+\.[0-9]+")
        # Issue with location: sometimes it is captured in the title of the report, in this case we will not catch it
        if len(response.css("div.polizeimeldung:not(first-child)::text").extract()) > 1:
            item["location"] = response.css("div.polizeimeldung:not(first-child)::text").extract()[1]
        else:
            item["location"] = response.css(".body > .text > .textile > p > strong::text").extract_first()
        event = response.css(".article > .body > .block > .body > .text > .textile > p::text").extract()
        event = [x.strip() for x in event]
        event = [x.replace("\n", "") for x in event]
        event = filter(None, event)
        item["event"] = event
        # We are done
        return item