#!/bin/bash


# hw4_run.sh $1=<treebank_filename> $2=<output_PCFG_file> \
#             $3=<test_sentence_filename> $4=<baseline_parse_output_filename> \
#             $5=<input_PCFG_file> \
#             $6=<improved_parse_output_filename> \
#             $7=<baseline_eval> $8=<improved_eval>

PYTHON=/opt/python-3.6/bin/python3

$PYTHON hw4_topcfg.py $1 $2
$PYTHON hw4_parser.py $2 $3 $4
$PYTHON hw4_improved_induction.py $1 $5
$PYTHON hw4_parser.py $5 $3 $6
sed -i.bak "s/\^\\S\+//g" $6
./tools/evalb -p ./tools/COLLINS.prm data/parses.gold $4 > $7
./tools/evalb -p ./tools/COLLINS.prm data/parses.gold $6 > $8
