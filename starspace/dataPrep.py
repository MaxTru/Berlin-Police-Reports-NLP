import os
import random

def extractRandom(n, infile, outfile):
    """Extracts n random lines from a file and stores them in outfile.

    Parameters
    ----------
    n : int
        random samples
    infile : string
        path to the file where the sample lines shall be taken from.
    outfile : string
        path to the file where the lines shall be saved.
    """
    # Open input file
    file_reader = open(os.path.abspath(infile), 'rb')

    # Prepare output payload file
    file_writer = open(os.path.abspath(outfile), "w+") #Create a file

    lines = file_reader.read().splitlines()

    # Write random lines
    file_writer.write("\n".join(random.sample(lines, n)))

    # Close out file
    file_writer.close()