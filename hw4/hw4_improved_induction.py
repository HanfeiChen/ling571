from typing import List, IO, Set
import nltk
import sys
from nltk import Tree
from collections import Counter

from nltk.grammar import Nonterminal, PCFG, ProbabilisticProduction, Production, is_terminal

def build_pcfg(treebank: List[Tree]):
    all_productions = []
    for tree in treebank:
        productions = extract_productions(tree)
        print(productions)
        all_productions.extend(productions)
    production_counter = Counter()
    lhs_counter = Counter()
    for production in all_productions:
        production_counter[production] += 1
        lhs_counter[production.lhs()] += 1
    production_probs = {k: v / (lhs_counter[k.lhs()]) for k, v in production_counter.items()}
    # print(production_probs)
    # for production, prob in production_probs.items():
    #     print(production, f'[{prob}]', file=file)
    prob_rules = [ProbabilisticProduction(k.lhs(), k.rhs(), prob=v) for k, v in production_probs.items()]
    start = Nonterminal(treebank[0].label())
    return PCFG(start, prob_rules)

def extract_productions(tree: Tree, parent: str = None):
    productions = []
    label = tree.label()
    if parent is not None:
        label_with_parent = label + '^' + parent
    else:
        label_with_parent = label
    rhs = []
    for child in tree:
        if isinstance(child, Tree):
            rhs.append(Nonterminal(child.label() + '^' + label))
            productions.extend(extract_productions(child, parent=label))
        else:
            rhs.append(child)
    # import pdb
    # pdb.set_trace()
    this_production = Production(Nonterminal(label_with_parent), tuple(rhs))
    productions.append(this_production)
    return productions


def load_treebank(file_path: str) -> List[Tree]:
    treebank = []
    with open(file_path, 'r') as f:
        for line in f:
            if len(line.strip()) > 0:
                tree = Tree.fromstring(line.strip())
                treebank.append(tree)
    return treebank


def get_nonterminal_symbol_set(grammar: PCFG) -> Set[str]:
    nonterminals = set()
    for rule in grammar.productions():
        nonterminals.add(rule.lhs().symbol())
    return nonterminals


def dump_grammar(grammar: PCFG, file: IO) -> None:
    start_symbol = grammar.start().symbol()
    lhs_symbols = [start_symbol] + \
            list(get_nonterminal_symbol_set(grammar) - {start_symbol})
    for lhs_symbol in lhs_symbols:
        rules = grammar.productions(lhs=Nonterminal(lhs_symbol))
        for rule in rules:
            print(rule, file=file)


if __name__ == '__main__':
    TREEBANK_FILE, OUTPUT_FILE = sys.argv[1:3]
    treebank = load_treebank(TREEBANK_FILE)
    with open(OUTPUT_FILE, 'w') as out_file:
        pcfg = build_pcfg(treebank)
        dump_grammar(pcfg, out_file)
