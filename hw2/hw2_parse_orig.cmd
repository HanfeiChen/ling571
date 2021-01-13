executable = /opt/python-3.6/bin/python3
getenv     = true
input      = hw2_parse_orig.in
output     = hw2_parse_orig.out
error      = hw2_parse_orig.error
log        = hw2_parse_orig.log
notification = complete
arguments  = "../hw1/hw1_parse.py atis.cfg sentences.txt hw2_orig_output.txt"
transfer_executable = false
request_memory = 2*1024
queue
