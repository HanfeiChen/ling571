import nltk
import sys

from nltk.tree import Tree

GRAMMAR_FILE, SENTENCES_FILE, OUTPUT_FILE = sys.argv[1:4]

grammar = nltk.data.load(GRAMMAR_FILE)
parser = nltk.parse.FeatureEarleyChartParser(grammar)

with open(SENTENCES_FILE, 'r') as in_file, open(OUTPUT_FILE, 'w') as out_file:
    num = 0
    for line in in_file:
        if len(line.strip()) > 0:
            num += 1
            line = line.strip()
            sent = line.split()
            parse: Tree = parser.parse_one(sent)
            # print(num, file=out_file)
            if parse is not None:
                print(parse._pformat_flat(nodesep='', parens='()', quotes=False), file=out_file)
                # print(parse, file=out_file)
            else:
                print(file=out_file)
