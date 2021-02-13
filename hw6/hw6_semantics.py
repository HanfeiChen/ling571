import nltk
import sys

from nltk.tree import Tree
from nltk import load_parser

GRAMMAR_FILE, SENTENCES_FILE, OUTPUT_FILE = sys.argv[1:4]

parser = load_parser(GRAMMAR_FILE, trace=0)

with open(SENTENCES_FILE, 'r') as in_file, open(OUTPUT_FILE, 'w') as out_file:
    num = 0
    for line in in_file:
        if len(line.strip()) > 0:
            num += 1
            line = line.strip()
            sent = line.split()
            parse: Tree = parser.parse_one(sent)
            print(line, file=out_file)
            if parse is not None:
                print(parse.label()['SEM'].simplify(), file=out_file)
                # print(parse, file=out_file)
            else:
                print(file=out_file)
