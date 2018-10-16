import scrapy

class PoliceReport(scrapy.Item):
    link = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    location = scrapy.Field()
    event = scrapy.Field()

class PoliceReportsSpider(scrapy.Spider):
    name = "police_reports_spider"
    start_urls = [
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2014/',
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2015/',
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2016/',
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2017/',
        'https://www.berlin.de/polizei/polizeimeldungen/archiv/2018/'
    ]
    BASE_URL='https://www.berlin.de'

    def parse(self, response):
        """Is called for the given start_urls."""
        links = response.css(".list-autoteaser li a").re(r'/polizei.+\.php')
        # Now, for every polce report we find, call a separate parse function
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_report)
        # Now, check whether there is another page with more reports, if so call that page and start crawling again
        next_page = response.css('.pager-item-next > a::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_report(selfself, response):
        """Is called for each police report found on the page"""
        item = PoliceReport()
        item["link"] = response.url
        item["title"] = response.css("h1.title::text").extract()
        item["date"] = response.css(".polizeimeldung::text").re("[0-9]+\.[0-9]+\.[0-9]+")
        # Issue with the location: sometimes it is captured in the title of the report, in this case we will not catch it
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