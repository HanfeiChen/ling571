import json
import codecs
import sys
from typing import Any, Dict, List
from collections import Counter

import nltk
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score


def load_glove_embeddings(file_path: str) -> Dict[str, np.array]:
    embeddings = dict()
    with open(file_path, 'r') as f:
        for line in f:
            values = line.split()
            embeddings[values[0]] = np.asarray(values[1:], dtype='float32')
    return embeddings


def load_relations_file(file_path: str) -> List:
    relations_file = codecs.open(file_path, 'r')
    return [json.loads(x) for x in relations_file]


def example_to_vector(example: Dict[str, Any], embeddings: Dict[str, np.array]) -> np.array:
    arg1_bow = sentence_to_bow_vec(example['Arg1']['RawText'], embeddings)
    arg2_bow = sentence_to_bow_vec(example['Arg2']['RawText'], embeddings)
    concat_vec = np.concatenate([arg1_bow, arg2_bow])
    return concat_vec


def example_to_sense(example: Dict[str, Any]) -> str:
    sense_labels = example['Sense']
    return sense_labels[0].split('.')[0]


def sentence_to_bow_vec(sentence: str, embeddings: Dict[str, np.array]) -> np.array:
    tokens = nltk.word_tokenize(sentence)
    token_embeddings = [embeddings[token.lower()]
                        for token in tokens
                        if token.lower() in embeddings]
    if len(token_embeddings) > 0:
        average_bow = np.mean(token_embeddings, axis=0)
    else:
        average_bow = np.zeros_like(embeddings['a'])
    return average_bow


def dump_vectors(vectors: List[np.array], senses: List[str], file_path: str) -> None:
    with open(file_path, 'w') as of:
        for vec, sense in zip(vectors, senses):
            print(','.join([str(num) for num in vec] + [sense]), file=of)


if __name__ == '__main__':

    GLOVE_EMBEDDING_FILE, \
        RELATION_TRAIN_DATA_FILE, \
        RELATION_TEST_DATA_FILE, \
        TRAIN_VECTOR_FILE, \
        TEST_VECTOR_FILE, \
        OUTPUT_RESULT_FILE = sys.argv[1:7]

    # GLOVE_EMBEDDING_FILE, \
    #     RELATION_TRAIN_DATA_FILE, \
    #     RELATION_TEST_DATA_FILE, \
    #     TRAIN_VECTOR_FILE, \
    #     TEST_VECTOR_FILE, \
    #     OUTPUT_RESULT_FILE = 'glove.6B.50d.txt relations_train.json relations_test.json hw9_training_vectors.txt hw9_test_vectors.txt hw9_output.txt'.split()

    print('Loading GloVe embeddings...')
    embeddings = load_glove_embeddings(GLOVE_EMBEDDING_FILE)

    print('Loading train relations file...')
    train_relations = load_relations_file(RELATION_TRAIN_DATA_FILE)

    print('Loading test relations file...')
    test_relations = load_relations_file(RELATION_TEST_DATA_FILE)

    print('Tokenizing and embedding train relations...')
    train_vectors = [example_to_vector(example, embeddings) for example in train_relations]
    train_labels = [example_to_sense(example) for example in train_relations]

    print('Tokenizing and embedding test relations...')
    test_vectors = [example_to_vector(example, embeddings) for example in test_relations]
    test_labels = [example_to_sense(example) for example in test_relations]

    print(Counter(train_labels))
    print(Counter(test_labels))

    labels = sorted(list(set(train_labels)))
    label_to_idx = {label: idx for idx, label in enumerate(labels)}

    dump_vectors(train_vectors, train_labels, TRAIN_VECTOR_FILE)
    dump_vectors(test_vectors, test_labels, TEST_VECTOR_FILE)

    X_train = train_vectors
    y_train = [label_to_idx[yi] for yi in train_labels]
    X_test = test_vectors
    y_test = [label_to_idx[yi] for yi in test_labels]

    clf = LogisticRegression()
    clf.fit(X_train, y_train)
    pred_test = clf.predict(X_test)
    per_class_f1_scores = f1_score(y_test, pred_test, average=None)

    with open(OUTPUT_RESULT_FILE, 'w') as of:
        print(per_class_f1_scores, file=of)
        for yi, pi in zip(y_test, pred_test):
            print(labels[yi], labels[pi], sep='\t', file=of)
