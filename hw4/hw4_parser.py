#!/usr/bin/env python3

from collections import defaultdict
import sys
from typing import Dict, List, Sequence, Tuple

import nltk
from nltk.grammar import PCFG, Nonterminal, ProbabilisticProduction, Production
from nltk.tree import Tree


def CKY_parse(tokens: List[str], grammar: PCFG) -> List[Tree]:
    table = defaultdict(float)
    back = dict()
    l = len(tokens)
    for j in range(1, l+1):
        rules: Sequence[ProbabilisticProduction] = grammar.productions(rhs=tokens[j-1])  # CNF, must be A -> word
        if len(rules) == 0:
            # failed to parse
            return None, 0.0

        for rule in rules:
            table[j-1, j, rule.lhs()] = rule.prob()

        for i in reversed(range(j-1)):
            for k in range(i+1, j):
                for rule in grammar.productions():
                    if len(rule.rhs()) == 2:
                        A = rule.lhs()
                        B, C = rule.rhs()
                        if table[i, k, B] > 0. and table[k, j, C] > 0:
                            if table[i, j, A] < rule.prob() * table[i, k, B] * table[k, j, C]:
                                table[i, j, A] = rule.prob() * table[i, k, B] * table[k, j, C]
                                back[i, j, A] = (k, B, C)
    if (0, l, grammar.start()) not in table:
        return None, 0.0
    best_prob = table[0, l, grammar.start()]
    tree = build_tree(back, tokens, 0, l, grammar.start(), 0)
    return tree, best_prob


def build_tree(back: Dict[Tuple[int, int, Nonterminal], Tuple[int, Nonterminal, Nonterminal]],
               tokens: List[str],
               left: int,
               right: int,
               root: Nonterminal,
               depth: int) -> List[Tree]:
    if left == right - 1:
        return Tree(root, [tokens[left]])
    split, left_root, right_root = back[left, right, root]
    left_tree = build_tree(back, tokens, left=left, right=split, root=left_root, depth=depth+1)
    right_tree = build_tree(back, tokens, left=split, right=right, root=right_root, depth=depth+1)
    return Tree(root, [left_tree, right_tree])


# This can be optimized using memoization.
# def table_to_parses(table: Dict[Tuple[int, int], Set[Tuple[Nonterminal, int]]],
#                     tokens: List[str],
#                     left: int,
#                     right: int,
#                     depth: int) -> List[Tree]:
#     parses = list()
#     print(f'{" " * depth}Parsing {left}...{right}: {tokens[left:right]}', file=sys.stderr)
#     for item, split in table[(left, right)]:
#         if split is None:
#             # parses.add(f'({item} {tokens[left]})')
#             parses.append(Tree(item, [tokens[left]]))
#         else:
#             left_parses = table_to_parses(table, tokens, left=left, right=split, depth=depth+1)
#             right_parses = table_to_parses(table, tokens, left=split, right=right, depth=depth+1)
#             for left_parse in left_parses:
#                 for right_parse in right_parses:
#                     # parses.add(f'({item} {left_parse} {right_parse})')
#                     parses.append(Tree(item, [left_parse, right_parse]))
#     return parses

def format_tree(tree: Tree) -> str:
    if not tree.children:
        return tree.label()
    elif len(tree.children) == 1:
        return f'({tree.label()} {tree.children[0]})'
    else:
        return f'({tree.label()} {tree.children[0]} {tree.children[1]})'

if __name__ == '__main__':
    INPUT_GRAMMAR_FILE, TEST_SENTENCES_FILE, OUTPUT_FILE = sys.argv[1:4]

    grammar = nltk.data.load(INPUT_GRAMMAR_FILE)

    with open(OUTPUT_FILE, 'w') as output_file:
        with open(TEST_SENTENCES_FILE, 'r') as test_file:
            for line in test_file:
                if len(line.strip()) > 0:
                    line = line.strip()
                    tokens = nltk.word_tokenize(line)
                    parse, prob = CKY_parse(tokens, grammar)
                    if parse is not None:
                        print(parse.pformat(margin=float('+inf')), file=output_file)
                    else:
                        print('()', file=output_file)
