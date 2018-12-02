#run locally in python console
import metapy
import os
idx = metapy.index.make_inverted_index(os.path.abspath("search/config.toml"))
# Build the query object and initialize a ranker
query = metapy.index.Document()
ranker = metapy.index.PivotedLength()
# To do an IR evaluation, we need to use the queries file and relevance judgements.
ev = metapy.index.IREval(os.path.abspath("search/config.toml"))
# We will loop over the queries file and add each result to the IREval object ev.
num_results = 10
with open('berlin-queries.txt') as query_file:
    for query_num, line in enumerate(query_file):
        query.content(unicode(line.strip()))
        results = ranker.score(idx, query, num_results)
        avg_p = ev.avg_p(results, query_num  + 1, num_results)
        print("Query {} average precision: {}".format(query_num + 1, avg_p))
ev.map()