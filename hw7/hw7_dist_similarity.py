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


def cosine_similarity(a, b) -> float:
    return 1. - distance.cosine(a, b)


class Vocabulary:
    def __init__(self, corpus: List[str]) -> None:
        self.idx2tok = list(set(corpus))
        self.tok2idx = {tok: idx for idx, tok in enumerate(self.idx2tok)}

    def __len__(self) -> int:
        return len(self.idx2tok)


def to_feature_vector(features: Dict[str, Union[int, float]], vocabulary: Vocabulary) -> np.array:
    vec = np.zeros(len(vocabulary))
    for feat, val in features.items():
        feat_idx = vocabulary.tok2idx[feat]
        vec[feat_idx] = val
    return vec


def count_neighbors(corpus: List[str], window: int) -> Dict[str, Counter]:
    corpus_len = len(corpus)
    neighbors = defaultdict(lambda: Counter())
    for i in trange(corpus_len):
        left_bound = max(0, i - window)
        right_bound = min(corpus_len - 1, i + window)
        for j in range(left_bound, right_bound + 1):
            if j != i:
                neighbors[corpus[i]][corpus[j]] += 1
    return neighbors


def compute_pmi(corpus: List[str], window: int) -> Dict[str, Dict[str, float]]:
    pmis = defaultdict(lambda: defaultdict(float))
    neighbors = count_neighbors(corpus, window)
    word_total = Counter()
    context_total = Counter()
    total = 0
    for word, word_neighbors in neighbors.items():
        for context, freq in word_neighbors.items():
            word_total[word] += freq
            context_total[context] += freq
            total += freq

    for word, word_neighbors in neighbors.items():
        for context, freq in word_neighbors.items():
            pij = freq / total
            pi = word_total[word] / total
            pj = context_total[context] / total
            pmi = math.log2(pij / (pi * pj))
            if pmi > 0.:
                pmis[word][context] = pmi
    return pmis


def dump_features(word: str, features: Dict[str, Union[int, float]]) -> str:
    out = word + ':'
    for f, v in sorted(features.items(), key=lambda x: -x[1])[:10]:
        out += f' {f}:{v}'
    return out


if __name__ == '__main__':
    WINDOW, WEIGHTING, JUDGMENT_FILENAME, OUTPUT_FILENAME = sys.argv[1:5]
    # WINDOW, WEIGHTING, JUDGMENT_FILENAME, OUTPUT_FILENAME = '2', 'FREQ', 'mc_similarity.txt', 'hw7_sim_2_FREQ_output.txt'
    # WINDOW, WEIGHTING, JUDGMENT_FILENAME, OUTPUT_FILENAME = '2', 'PMI', 'mc_similarity.txt', 'hw7_sim_2_PMI_output.txt'
    # WINDOW, WEIGHTING, JUDGMENT_FILENAME, OUTPUT_FILENAME = '10', 'PMI', 'mc_similarity.txt', 'hw7_sim_10_PMI_output.txt'
    WINDOW = int(WINDOW)

    nltk.download('brown')
    corpus: List[str] = nltk.corpus.brown.words()
    corpus = [token.lower() for token in corpus if re.match('^\\w+$', token)]
    vocabulary = Vocabulary(corpus)

    if WEIGHTING == 'FREQ':
        features = count_neighbors(corpus, WINDOW)
    elif WEIGHTING == 'PMI':
        features = compute_pmi(corpus, WINDOW)

    with open(JUDGMENT_FILENAME, 'r') as jf, open(OUTPUT_FILENAME, 'w') as of:
        sys_scores, human_scores = [], []
        for line in jf:
            if len(line.strip()) > 0:
                line = line.strip()
                w1, w2, score = line.split(',')
                score = float(score)
                fv1 = to_feature_vector(features[w1], vocabulary)
                fv2 = to_feature_vector(features[w2], vocabulary)
                sim = cosine_similarity(fv1, fv2)
                print(dump_features(w1, features[w1]), file=of)
                print(dump_features(w2, features[w2]), file=of)
                print(f'{w1},{w2}:{sim}', file=of)
                sys_scores.append(sim)
                human_scores.append(score)
        correlation = stats.spearmanr(sys_scores, human_scores).correlation
        print(f'Correlation:{correlation}', file=of)
