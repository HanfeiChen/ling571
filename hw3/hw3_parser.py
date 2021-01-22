#!/usr/bin/env python3

from collections import defaultdict
import sys
from typing import Dict, List, Sequence, Set, Tuple

import nltk
from nltk.grammar import CFG, Nonterminal, Production
from nltk.tree import Tree


def CKY_parse(tokens: List[str], grammar: CFG) -> List[Tree]:
    table = defaultdict(set)
    l = len(tokens)
    for j in range(1, l+1):
        rules: Sequence[Production] = grammar.productions(rhs=tokens[j-1])  # CNF, must be A -> word
        if len(rules) == 0:
            # failed to parse
            return []

        for rule in rules:
            table[j-1, j].add((rule.lhs(), None))

        for i in reversed(range(j-1)):
            for k in range(i+1, j):
                for B, _ in table[i, k]:
                    for C, _ in table[k, j]:
                        for rule in grammar.productions():
                            if tuple(rule.rhs()) == (B, C):
                                table[i, j].add((rule.lhs(), k))
    table[0, l] = {el for el in table[0, l] if el[0] == grammar.start()}
    parses = table_to_parses(table, tokens, left=0, right=l, depth=0)
    return parses


# This can be optimized using memoization.
def table_to_parses(table: Dict[Tuple[int, int], Set[Tuple[Nonterminal, int]]],
                    tokens: List[str],
                    left: int,
                    right: int,
                    depth: int) -> List[Tree]:
    parses = list()
    print(f'{" " * depth}Parsing {left}...{right}: {tokens[left:right]}', file=sys.stderr)
    for item, split in table[(left, right)]:
        if split is None:
            # parses.add(f'({item} {tokens[left]})')
            parses.append(Tree(item, [tokens[left]]))
        else:
            left_parses = table_to_parses(table, tokens, left=left, right=split, depth=depth+1)
            right_parses = table_to_parses(table, tokens, left=split, right=right, depth=depth+1)
            for left_parse in left_parses:
                for right_parse in right_parses:
                    # parses.add(f'({item} {left_parse} {right_parse})')
                    parses.append(Tree(item, [left_parse, right_parse]))
    return parses


if __name__ == '__main__':
    INPUT_GRAMMAR_FILE, TEST_SENTENCES_FILE, OUTPUT_FILE = sys.argv[1:4]

    grammar = nltk.data.load(INPUT_GRAMMAR_FILE)

    with open(OUTPUT_FILE, 'w') as output_file:
        with open(TEST_SENTENCES_FILE, 'r') as test_file:
            for line in test_file:
                if len(line.strip()) > 0:
                    line = line.strip()
                    print(line, file=output_file)
                    tokens = nltk.word_tokenize(line)
                    parses = CKY_parse(tokens, grammar)
                    for parse in parses:
                        print(parse, file=output_file)
                    print('Number of parses:', len(parses), file=output_file)
                    print(file=output_file)
