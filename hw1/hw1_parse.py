#!/usr/bin/env python

import nltk
import sys

GRAMMAR_FILE, TEST_SENTENCE_FILE, OUTPUT_FILE = sys.argv[1:4]

grammar = nltk.data.load(GRAMMAR_FILE)
parser = nltk.parse.EarleyChartParser(grammar)

all_num_parses = []

with open(TEST_SENTENCE_FILE, 'r') as in_file, \
     open(OUTPUT_FILE, 'w') as out_file:
    for line in in_file:
        if len(line.strip()) > 0:
            sentence = line.strip()
            print(sentence, file=out_file)
            tokens = nltk.word_tokenize(sentence)
            parsed = parser.parse(tokens)
            num_parses = 0
            for item in parsed:
                num_parses += 1
                print(item, file=out_file)
            print(f'Number of parses: {num_parses}', file=out_file)
            all_num_parses.append(num_parses)
            print(file=out_file)

    avg_num_parses = sum(all_num_parses) / len(all_num_parses)
    print(f'Average parses per sentence: {avg_num_parses:.3f}', file=out_file)
