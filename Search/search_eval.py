import math
import sys
import time
import metapy
import pytoml


class myranker(metapy.index.RankingFunction):

    def __init__(self, some_param1=1.2, some_param2=0.75, some_param3=500, some_param4=1.4):
        self.k1 = some_param1
        self.b = some_param2
        self.k3 = some_param3
        self.d = some_param4

        super(myranker, self).__init__()

    def score_one(self, sd):
        """"BM25+ implementation"""
        term1 = ((self.k3 + 1)*sd.query_term_weight)/(self.k3 + sd.query_term_weight)
        numerator = (self.k1 + 1)*sd.doc_term_count
        denominator = sd.doc_term_count + self.k1*(1 - self.b + self.b*(sd.doc_size / sd.avg_dl))
        term2 = numerator/denominator + self.d
        term3 = math.log2((sd.num_docs + 1)/sd.doc_count)
        return term1*term2*term3

def load_ranker(cfg_file):
    return myranker()
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} config.toml".format(sys.argv[0]))
        sys.exit(1)

    cfg = sys.argv[1]
    print('Building or loading index...')
    idx = metapy.index.make_inverted_index(cfg)
    ranker = load_ranker(cfg)
    ev = metapy.index.IREval(cfg)

    with open(cfg, 'r') as fin:
        cfg_d = pytoml.load(fin)

    query_cfg = cfg_d['query-runner']
    if query_cfg is None:
        print("query-runner table needed in {}".format(cfg))
        sys.exit(1)

    start_time = time.time()
    top_k = 10
    query_path = query_cfg.get('query-path', 'queries.txt')
    query_start = query_cfg.get('query-id-start', 0)

    query = metapy.index.Document()
    print('Running queries')
    with open(query_path) as query_file:
        for query_num, line in enumerate(query_file):
            query.content(line.strip())
            results = ranker.score(idx, query, top_k)
            avg_p = ev.avg_p(results, query_start + query_num, top_k)
            print("Query {} average precision: {}".format(query_num + 1, avg_p))
    print("Mean average precision: {}".format(ev.map()))
    print("Elapsed: {} seconds".format(round(time.time() - start_time, 4)))
