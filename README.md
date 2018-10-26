# Berlin-Police-Reports-NLP

**-------------Work in Progress-------------**

# Required Packages
* Click
* Flask
* Flask-WTF
* Jinja2
* WTForms
* Scrapy

# Project structure
The project contains three key modules:
1. Scrapy Webscraper **/scraper**
2. Flask WebUI **/webui**
3. Dataset (see _Dataset_) **/data**

# Dataset
#### Source and Description
The Police Reports in this demo application are scraped from the following URIs:
* 'https://www.berlin.de/polizei/polizeimeldungen/archiv/2014/'
* 'https://www.berlin.de/polizei/polizeimeldungen/archiv/2015/'
* 'https://www.berlin.de/polizei/polizeimeldungen/archiv/2016/'
* 'https://www.berlin.de/polizei/polizeimeldungen/archiv/2017/'
* 'https://www.berlin.de/polizei/polizeimeldungen/archiv/2018/'

The following attributes of a Police Report are considered in this demo application:
1. date
2. title
3. link
4. event
5. location

#### Dataset used in this demo project
The Dataset for the demo application was scraped on the 18th October 2018. The raw scraped data can be found under *data/reports_raw_2018-10-19.dat*.

The initial Dataset (9852 reports) was cleaned using OpenRefine as following:
1. Removed duplicates (#3)
2. Removed reports with empty event description (#19)

The resulting cleaned Dataset can be found under *data/reports_cleaned_2018-10-21.dat*. Further, the cleaned Dataset was split into a file for the payload (the title of the report + ". " + the description) and a file for the metadata respectively (date, location and link). This split allows for easier further processing.

