import metapy
import os

class Searcher:
    def __init__(self):
        self.idx = metapy.index.make_inverted_index(os.path.abspath("search/config.toml"))
        self.ranker = metapy.index.OkapiBM25()

    def search(self, query_text):
        query = metapy.index.Document()
        query.content(query_text)
        print(self.ranker.score(self.idx, query))

if __name__ == "__main__":
    searcher = Searcher()
    while True:
        try:
            query = raw_input("")
        except EOFError:
            break
        searcher.search(query)