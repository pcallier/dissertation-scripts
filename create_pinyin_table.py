#!/usr/bin/env python
# encoding: utf-8
"""
create_pinyin_table.py
"""
import sys
import subprocess

table_filename = sys.argv[1]

# the chinese should be in the 6th column
# and it comes with a newline attached
table_file = open(table_filename)
table_rows = table_file.readlines()
table_elements = [r.split('\t') for r in table_rows]

# call the conversion script
for t_row in range(0, len(table_elements)):
    to_convert = table_elements[t_row][5].strip()
    
    conversion_process = subprocess.Popen(['./convert_to_pinyin.py', to_convert],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    (pinyin_string, any_errors) = conversion_process.communicate()
    if any_errors: print >> sys.stderr, any_errors
    
    #print >> sys.stderr, pinyin_string
    #print >> sys.stderr, table_elements[t_row][0:5]
    new_row = ('\t'.join(table_elements[t_row][0:5]) + '\t').decode('utf-8') + pinyin_string.strip().decode('utf-8')
    print new_row.encode('utf-8')
    
    
