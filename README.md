# README IS CURRENTLY WORK IN PROGRESS

# Berlin-Police-Reports-NLP
# "Who needs this and why?"
The Berlin (Germany) Police regularly publishes Police reports with significance for the public (~5-10 per day). They include from car accident to murder. The reports are publically available online since 2014: https://www.berlin.de/polizei/polizeimeldungen/archiv/​. However, the archive does not offer a search engine or any sort of categorization (besides years). Therefore the usability of this archive for journalists or citizens is very limited.
 
This project implements a Web GUI which allows the user to effectively search and filter these police reports by utilizing WebScraping, Information Retrieval and Text Classification technologies. The ultimate goal is to increase the usability of the Web Archive for journalists or interested citizens.

# Project structure
The project structure follows the key components of this project:
1. Scrapy Webscraper **/scraper**
2. Flask WebUI **/webui**
3. Dataset (for additional information see _Dataset_) **/data**
4. Starspace (for additional information see _Starspace_) **/starspace**
5. MetaPy Search implementation **/search**

# Architecture
The application consists of four components: 
1. **Scrapy WebCrawler**: Crawler for scraping the police reports since 2014 from the official archive. After scraping, the reports are post-processed (incl. split of payload and metadata, ISO date-transformation, ...) so to have a clean dataset for subsequent text classification and information retrieval. At startup of the WebUI, the reports are loaded into a SQLite database by the Flask application (supported by SQLAlchemy). The WebCrawling needs to be initiated manually, post-processing is automated.
2. **Flask WebUI**: WebUI allowing the user to search for police reports, browse police reports or filter police reports by their class / category. This is the core component for the end-user. The WebUI accesses the reports in a SQLite DB (supported by SQLAlchemy).
3. **StarSpace Text Classification**: Neural embedding model used to classify the police reports. The classification needs to be initiated manually after a new dataset was loaded.  
4. **MeTAPy Information Retrieval**: To retrieve relevant documents (police reports) for a user specified query, the MeTA Toolkit is used. This is directly integrated into the Flask WebUI using the MeTAPy module. After startup of the application and prior to the first search, MeTAPy builds an inverted index as basis for the later document retrieval.

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

# Usage
#### Requirements
**WebUI**: To run the core component of this project - the WebUI - a working Python environment is required. The project was tested on Python 2.7. Full module requirements can be found in _requirements.txt_.

_The following components of this project are optional to run, since they are only used to create a clean dataset for the WebUI. A clean dataset is already provided (see _/data_)._

**Scraper**: To run the WebScraper a working Python environment is required. Besides Python, the data post-processing also requires a bash shell.

**StarSpace**: To run the document classification with StarSpace a Linux environment and a a clone of the StarSpace Git repository (https://github.com/facebookresearch/Starspace.git) is required.

#### How to use
***A tutorial how to run this project will be added later***

# Authors and Contribution
* Project Lead, Architecture, WebScraper, WebUI, TextClassification, Documentation: **Maximilian Trumpf**
* Support and Search: **Saurav Chetry**

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

##### MeTA Toolkit and MeTAPy
https://meta-toolkit.org/
https://github.com/meta-toolkit/metapy/ 

