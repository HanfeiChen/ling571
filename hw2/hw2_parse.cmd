executable = /opt/python-3.6/bin/python3
getenv     = true
input      = hw2_parse.in
output     = hw2_parse.out
error      = hw2_parse.error
log        = hw2_parse.log
notification = complete
arguments  = "../hw1/hw1_parse.py hw2_grammar_cnf.cfg sentences.txt hw2_cnf_output.txt"
transfer_executable = false
request_memory = 2*1024
queue
