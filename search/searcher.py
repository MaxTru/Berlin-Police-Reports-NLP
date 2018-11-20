"""Searcher class implements the IR functionality."""
import metapy
import os
import sys

class Searcher:
    def __init__(self):
        self.idx = metapy.index.make_inverted_index(os.path.abspath("search/config.toml"))
        self.ranker = metapy.index.OkapiBM25()

    def search(self, query_text):
        """A user may search for a query_text and retrieve the relevant reports including their score.
        Returns
        -------
        Returns the String representation of the relevant reports including their score in stdout.
        stdout is needed since we start the searcher as separate process and communicate with that process using
        stdin and stdout. This is to work around a bug where metapy will block Flask when run inside a Flask route."""
        query = metapy.index.Document()
        query.content(query_text, encoding="utf-8")
        print(self.ranker.score(self.idx, query, 100))

if __name__ == "__main__":
    searcher = Searcher()
    while True:
        try:
            query = raw_input("").decode(sys.stdin.encoding)
        except EOFError:
            break
        searcher.search(query)