"""Utility functions to handle policereports files. Policereports file scraped from the web need the following format:
Columns: date,title,link,event,location
Header: yes

They can be created by running policeReportsSpider.py using Scrapy.
"""
import csv, os, exceptions

def extract_payload(infile, outfile):
    """Utility method to extract the metadata of a scraped policereports file and store only the metadata to another file.

    Parameters
    ----------
    infile : string
        path to the scraped police reports file. Format: csv. date,title,link,event,location. Assumes a header.
    outfile : string
        path and filename of the file where the metadata shall be written to. File will be created if not existing. Existing file will be overwritten.

    Returns
    -------
    Null
    """
    # Open input file
    file_reader = csv.reader(open(os.path.abspath(infile), 'rb'))

    #Prepare output payload file
    file_writer = open(os.path.abspath(outfile), "w+") #Create a file

    # Extract and write payload
    file_reader.next() # Skip first (header) line
    for row in file_reader:
        file_writer.write(row[1] + ". "+ row[3] + "\n")

    #Close out file
    file_writer.close()

def extract_metadata(infile, outfile):
    """Utility method to extract the metadata of a scraped policereports file and store only the metadata to another file.

    Parameters
    ----------
    infile : string
        path to the scraped police reports file. Format: csv. date,title,link,event,location. Assumes a header.
    outfile : string
        path and filename of the file where the metadata shall be written to. File will be created if not existing. Existing file will be overwritten.

    Returns
    -------
    Null
    """
    # Open input file
    file_reader = csv.reader(open(os.path.abspath(infile), 'rb'))

    #Prepare output payload file
    file_writer = open(os.path.abspath(outfile), "w+") #Create a file

    # Extract and write metadata
    file_reader.next() # Skip first (header) line
    for row in file_reader:
        file_writer.write(row[0] + "," + row[2] + "," + row[4] + "\n")

    #Close out file
    file_writer.close()

def combined_access_report(reportsfile, metadatafile, reportid):
    """Utility method to access a particular police report including its metadata as dictionary.

    Parameters
    ----------
    reportsfile : string
        path to the file which was created using extract_payload(...)
    metadatafile : string
        path to the file which was created using extract_metadata(...)
    reportid : int
        ID of the report to be accessed. IDs are assumed based on the flatfile (line 0 equals ID 0)

    Returns
    -------
    dict
        "date": string
        "title": string
        "link": string
        "event": string
        "location": string
    """
    reports_lines= open(os.path.abspath(reportsfile), "r").readlines()
    metadata_lines = open(os.path.abspath(metadatafile), "r").readlines()
    if reportid >= len(reports_lines) \
            or reportid < 0 \
            or len(reports_lines) != len(metadata_lines):
        raise IndexError("Invalid reportid or input files with different lenghts.")
    else:
        return {
            "date": metadata_lines[reportid].split(",")[0].strip().decode("utf-8"),
            "title": reports_lines[reportid][:reports_lines[reportid].index(".")].strip().decode("utf-8"),
            "link": metadata_lines[reportid].split(",")[1].strip().decode("utf-8"),
            "event": reports_lines[reportid][reports_lines[reportid].index(".") + 1:].strip().strip().decode("utf-8"),
            "location": metadata_lines[reportid].split(",")[2].strip().decode("utf-8"),
            "id": reportid
        }

def combined_access_report_labels(reportsfile, metadatafile, labelfile, reportid):
    """Utility method to access a particular police report including its metadata and its label as dictionary.

    Parameters
    ----------
    reportsfile : string
        path to the file which was created using extract_payload(...)
    metadatafile : string
        path to the file which was created using extract_metadata(...)
    labelfile : string
        path to the file which contains the labels for all police reports
    reportid : int
        ID of the report to be accessed. IDs are assumed based on the flatfile (line 0 equals ID 0)

    Returns
    -------
    dict
        "date": string
        "title": string
        "link": string
        "event": string
        "location": string
        "label": string
    """
    reports_lines = open(os.path.abspath(reportsfile), "r").readlines()
    metadata_lines = open(os.path.abspath(metadatafile), "r").readlines()
    label_lines = open(os.path.abspath(labelfile), "r").readlines()
    if reportid >= len(reports_lines) \
            or reportid < 0 \
            or len(reports_lines) != len(metadata_lines) \
            or len(reports_lines) != len(label_lines):
        raise IndexError("Invalid reportid or input files with different lenghts.")
    else:
        return {
            "date": metadata_lines[reportid].split(",")[0].strip().decode("utf-8"),
            "title": reports_lines[reportid][:reports_lines[reportid].index(".")].strip().decode("utf-8"),
            "link": metadata_lines[reportid].split(",")[1].strip().decode("utf-8"),
            "event": reports_lines[reportid][reports_lines[reportid].index(".") + 1:].strip().decode("utf-8"),
            "location": metadata_lines[reportid].split(",")[2].strip().decode("utf-8"),
            "id": reportid,
            "label": label_lines[reportid].strip().decode("utf-8")
        }