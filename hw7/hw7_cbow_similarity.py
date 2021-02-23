import sys
import re
import math
from collections import defaultdict, Counter
from typing import Dict, List, IO, Union

import nltk
import numpy as np
from tqdm import trange
from scipy import stats
from scipy.spatial import distance
from gensim.models import Word2Vec


def cosine_similarity(a, b) -> float:
    return 1. - distance.cosine(a, b)


if __name__ == '__main__':
    WINDOW, JUDGMENT_FILENAME, OUTPUT_FILENAME = sys.argv[1:4]
    # WINDOW, JUDGMENT_FILENAME, OUTPUT_FILENAME = '2', 'mc_similarity.txt', 'hw7_sim_2_CBOW_output.txt'
    WINDOW = int(WINDOW)

    corpus: List[str] = nltk.corpus.brown.words()
    corpus = [token.lower() for token in corpus if re.match('^\\w+$', token)]
    model = Word2Vec([corpus], window=WINDOW, min_count=1)

    with open(JUDGMENT_FILENAME, 'r') as jf, open(OUTPUT_FILENAME, 'w') as of:
        sys_scores, human_scores = [], []
        for line in jf:
            if len(line.strip()) > 0:
                line = line.strip()
                w1, w2, score = line.split(',')
                score = float(score)
                v1 = model.wv[w1]
                v2 = model.wv[w2]
                sim = cosine_similarity(v1, v2)
                print(f'{w1},{w2}:{sim}', file=of)
                sys_scores.append(sim)
                human_scores.append(score)
        correlation = stats.spearmanr(sys_scores, human_scores).correlation
        print(f'Correlation:{correlation}', file=of)
