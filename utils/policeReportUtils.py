"""Utility functions to handle policereports files. Policereports file scraped from the web need the following format:
Columns: date,title,link,event,location
Header: yes
"""
import csv, os

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
    outfile : string
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

    return {
        "date": metadata_lines[reportid].split(",")[0],
        "title": reports_lines[reportid][:reports_lines[reportid].index(".")],
        "link": metadata_lines[reportid].split(",")[1],
        "event": reports_lines[reportid][reports_lines[reportid].index(".") + 1:].strip(),
        "location": metadata_lines[reportid].split(",")[2]
    }

