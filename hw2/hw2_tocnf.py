#!/usr/bin/env python3

import nltk
import sys
from collections import deque
from typing import IO, List, Set, Union

from nltk.grammar import CFG, Nonterminal, Production, is_nonterminal, is_terminal


INPUT_GRAMMAR_FILE, OUTPUT_GRAMMAR_FILE = sys.argv[1:3]


used_nonterminal_symbols: Set[str] = set()
curr_new_nonterminal_index = 0


def get_nonterminal_symbol_set(grammar: CFG) -> Set[str]:
    nonterminals = set()
    for rule in grammar.productions():
        nonterminals.add(rule.lhs().symbol())
    return nonterminals


def use_new_nonterminal() -> Nonterminal:
    global curr_new_nonterminal_index
    prefix = 'X'
    while f'_{prefix}{curr_new_nonterminal_index}_' in used_nonterminal_symbols:
        curr_new_nonterminal_index += 1
    new_nonterminal_symbol = f'_{prefix}{curr_new_nonterminal_index}_'
    used_nonterminal_symbols.add(new_nonterminal_symbol)
    return Nonterminal(new_nonterminal_symbol)


def contains_unit_production(grammar: CFG) -> bool:
    for rule in grammar.productions():
        if len(rule.rhs()) == 1 and is_nonterminal(rule.rhs()[0]):
            print(f'{rule} is still a unit production')
            return True
    return False


def is_cnf_conforming(rule: Production) -> bool:
    rhs = rule.rhs()
    if len(rhs) == 2:
        return all(is_nonterminal(x) for x in rhs)
    if len(rhs) == 1:
        return is_terminal(rhs[0])
    return False


def convert_to_cnf(grammar: CFG) -> CFG:
    # break down hybrid rules
    new_rules: List[Production] = []
    print('Eliminating hybrid rules')
    for rule in grammar.productions():
        if is_cnf_conforming(rule):
            # print(f'{rule} is conforming', file=sys.stderr)
            new_rules.append(rule)
        else:
            new_rhs: List[Nonterminal] = []
            for x in rule.rhs():
                if is_terminal(x):
                    dummy_nonterminal = use_new_nonterminal()
                    dummy_rule = Production(dummy_nonterminal, [x])
                    new_rhs.append(dummy_nonterminal)
                    new_rules.append(dummy_rule)
                else:
                    new_rhs.append(x)
            new_rule = Production(rule.lhs(), new_rhs)
            new_rules.append(new_rule)
    grammar = CFG(grammar.start(), new_rules)

    # repeatedly resolve unit productions
    print('Eliminating unit productions')
    while contains_unit_production(grammar):
        new_rules: List[Production] = []
        for rule in grammar.productions():
            # for each rule, we try to eliminate one folded unit production
            new_rules.extend(unit_production_conversion_step(rule, grammar))
        grammar = CFG(grammar.start(), new_rules)

    # break down long rules
    print('Eliminating long rules')
    new_rules = []
    for rule in grammar.productions():
        if len(rule.rhs()) > 2:
            new_rules.extend(long_rule_conversion(rule))
        else:
            new_rules.append(rule)
    grammar = CFG(grammar.start(), new_rules)

    return grammar


def unit_production_conversion_step(rule: Production, grammar: CFG) -> List[Production]:
    if len(rule.rhs()) > 1 or is_terminal(rule.rhs()[0]):
        return [rule]
    new_rules: List[Production] = []
    mid = rule.rhs()[0]
    for next_rule in grammar.productions(lhs=mid):
        new_rules.append(Production(rule.lhs(), next_rule.rhs()))
    if len(new_rules) == 0:
        # failed to resolve, keep original
        return [rule]
    print(f'Converted {rule} to {len(new_rules)} rules: {new_rules}')
    return new_rules


def unit_production_conversion(rule: Production, grammar: CFG) -> List[Production]:
    if len(rule.rhs()) > 1 or is_terminal(rule.rhs()[0]):
        return [rule]
    new_rules: List[Production] = []
    q = deque()
    rhs: Union[str, Nonterminal] = rule.rhs()[0]
    q.append(rhs)
    seen = set()
    while len(q):
        current = q.popleft()
        seen.add(current)
        if is_terminal(current):
            new_rules.append(Production(rule.lhs(), [current]))
            continue
        next_rules: List[Production] = grammar.productions(lhs=current)
        for next_rule in next_rules:
            if len(next_rule.rhs()) == 1:
                rhs = next_rule.rhs()[0]
                if rhs not in seen:
                    q.append(rhs)
    if len(new_rules) == 0:
        # failed to resolve, return original
        print(f'Failed to resolve {rule}')
        return [rule]
    return new_rules


def long_rule_conversion(rule: Production) -> List[Production]:
    if len(rule.rhs()) < 3:
        return [rule]
    # print(f'Long rule conversion on {rule}', file=sys.stderr)
    rhs = deque(rule.rhs())
    new_rules: List[Production] = []
    current = rhs.pop()
    while len(rhs) > 1:
        merged = rhs.pop()
        new_lhs = use_new_nonterminal()
        new_rule = Production(new_lhs, [merged, current])
        new_rules.append(new_rule)
        current = new_lhs
    new_rule = Production(rule.lhs(), [rhs.pop(), current])
    new_rules.append(new_rule)
    return new_rules


def dump_grammar(grammar: CFG, file: IO) -> None:
    start_symbol = grammar.start().symbol()
    lhs_symbols = [start_symbol] + \
            list(get_nonterminal_symbol_set(grammar) - {start_symbol})
    for lhs_symbol in lhs_symbols:
        rules = grammar.productions(lhs=Nonterminal(lhs_symbol))
        rules = [str(rule) for rule in rules]
        rules = [rule.split('->')[1].strip() for rule in rules]
        rules = ' | '.join(rules)
        print(f"{lhs_symbol} -> {rules}", file=file)



grammar = nltk.data.load(INPUT_GRAMMAR_FILE)
nonterminal_symbols = get_nonterminal_symbol_set(grammar)
used_nonterminal_symbols |= nonterminal_symbols

cnf = convert_to_cnf(grammar)

with open(OUTPUT_GRAMMAR_FILE, 'w') as out_file:
    dump_grammar(cnf, out_file)
