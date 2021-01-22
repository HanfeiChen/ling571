executable = hw3_parser.sh
getenv     = true
input      = hw3_parser.in
output     = hw3_parser.out
error      = hw3_parser.error
log        = hw3_parser.log
notification = complete
arguments  = "grammar_cnf.cfg sentences.txt hw3_output.txt"
transfer_executable = false
request_memory = 2*1024
queue
