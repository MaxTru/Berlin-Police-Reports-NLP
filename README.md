# Berlin-Police-Reports-NLP

**-------------Work in Progress-------------**

# Required Packages
* Click
* Flask
* Flask-WTF
* Jinja2
* WTForms
* Scrapy 
* Metapy
* Flask-SQLAlchemy
# Project structure
The project contains three key modules:
1. Scrapy Webscraper **/scraper**
2. Flask WebUI **/webui**
3. Dataset (see _Dataset_) **/data**
4. Starspace (see _Starspace_) **/starspace**

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
3. Formatted dates in Metadate according to ISO 8601 (see *data/ISO_transform_date.sh*)
4. Cleaned up the date field in some cases where 2 dates where stated (see *data/Clear_double_dates.sh*)

The resulting cleaned Dataset can be found under *data/reports_cleaned_2018-10-21.dat*. Further, the cleaned Dataset was split into a file for the payload (Title and event; filename: _data.dat_) and a file for the metadata respectively (date, location and link). This split allows for easier further processing.

# StarSpace
#### Idea
StarSpace is used in this project to perform a document classification on all police reports. In this first demo, three classes were defined:
1. Traffic Offense
2. Violent Crime
3. Criminal Damage or Fire

#### Example
A training dataset with random n=500 docs and a test dataset with random n=250 documents. The entire document tokenization, training, testing and prediction is performed in the script _train_and_apply_model.sh_. The script must be run in a directory where StarSpace is located (see https://github.com/facebookresearch/StarSpace/). The predictions are picked up in the Flask WebApp to allow the user to browse police reports by document class (see 3 classes mentioned before).

# Sources
##### StarSpace
```
@article{wu2017starspace,
  title={StarSpace: Embed All The Things!},
  author = {{Wu}, L. and {Fisch}, A. and {Chopra}, S. and {Adams}, K. and {Bordes}, A. and {Weston}, J.},
  journal={arXiv preprint arXiv:{1709.03856}},
  year={2017}
}
```
##### German Stopwords
https://github.com/solariz/german_stopwords/blob/master/german_stopwords_full.txt

