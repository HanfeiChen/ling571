import sys
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

from nltk.corpus import wordnet_ic
from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset, information_content

from scipy import stats


def resnik_similarity(probe_word, context_noun, ic) -> Tuple[Optional[Synset], float]:
    probe_synsets: List[Synset] = wn.synsets(probe_word)
    context_synsets: List[Synset] = wn.synsets(context_noun, pos=wn.NOUN)
    similarity = 0.
    sense: Optional[Synset] = None
    for probe_synset in probe_synsets:
        for context_synset in context_synsets:
            subsumers = probe_synset.lowest_common_hypernyms(context_synset)
            max_ic = 0.0 if len(subsumers) == 0 else max(information_content(lcs, ic) for lcs in subsumers)
            if max_ic > similarity:
                similarity = max_ic
                sense = probe_synset
    return sense, similarity


def load_wsd_test_data(file_name: str) -> List[Tuple[str, List[str]]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            if len(line.strip()) > 0:
                line = line.strip()
                probe_word, noun_group = line.split()
                noun_group = list(noun_group.split(','))
                data.append((probe_word, noun_group))
    return data


def load_judgment_file(file_name: str) -> List[Tuple[str, str, float]]:
    data = []
    with open(file_name, 'r') as f:
        for line in f:
            if len(line.strip()) > 0:
                line = line.strip()
                w1, w2, score = line.split(',')
                score = float(score)
                data.append((w1, w2, score))
    return data


if __name__ == '__main__':
    IC_TYPE, WSD_TEST_FILE, JUDGMENT_FILE, OUTPUT_FILE = sys.argv[1:5]
    # IC_TYPE, WSD_TEST_FILE, JUDGMENT_FILE, OUTPUT_FILE = 'nltk wsd_contexts.txt mc_similarity.txt hw8_output.txt'.split()

    if IC_TYPE == 'nltk':
        ic_data: Dict = wordnet_ic.ic('ic-brown-resnik-add1.dat')
    else:
        raise NotImplementedError

    wsd_test_data = load_wsd_test_data(WSD_TEST_FILE)
    judgment_data = load_judgment_file(JUDGMENT_FILE)

    with open(OUTPUT_FILE, 'w') as out_file:
        for probe_word, noun_group in wsd_test_data:
            noun_sense_similarity_triples = []
            for context_noun in noun_group:
                sense, similarity = resnik_similarity(probe_word, context_noun, ic_data)
                noun_sense_similarity_triples.append((context_noun, sense, similarity))
            votes = defaultdict(float)
            for _, sense, similarity in noun_sense_similarity_triples:
                if sense is not None:
                    votes[sense.name()] += similarity
            best_sense = max(votes, key=votes.get)
            print(' '.join([f'({probe_word}, {noun}, {similarity})'
                            for noun, _, similarity
                            in noun_sense_similarity_triples]), file=out_file)
            print(best_sense, file=out_file)

        human_scores, sys_scores = [], []
        for w1, w2, score in judgment_data:
            _, sys_score = resnik_similarity(w1, w2, ic_data)
            print(f'{w1},{w2}:{sys_score}', file=out_file)
            human_scores.append(score)
            sys_scores.append(sys_score)
        print(f'Correlation:{stats.spearmanr(sys_scores, human_scores).correlation}', file=out_file)
