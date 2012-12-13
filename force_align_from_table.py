#!/usr/bin/env python
# encoding: utf-8
"""
    force_align_from_table.py
    
    Given a table of the sort one gets from ELAN,
    where there is text in the 6th column and
    timestamps in the 2nd and 3rd columns, do the following:
    
    1. Create a custom dictionary with all and only the legit pinyin
    syllables in the data?
    2. [Unnecessary, align.py can align portions] Use sendpraat to do some trickery, i.e.
        a. open the sound file
        b. segment out the current segment to be aligned
        c. save it as WAV
    3. Make a text file of that segment's transcript
    4. Clean up that text file! replace/delete stray symbols,
        add silences, noises, breaths? [this is done before 1]
    5. Align that file+transcript
    6. Add the textgrid's distinctiveness to your own. Grow and improve. (Concatenate)
    
"""

import re
import sys
import os
import shutil
import codecs
import subprocess
import time


table_filename = "test_table.txt"
p2fa_path = "/home/patrick/downloads/p2fa"
sound_path = "/home/patrick/sf_Patrick/Documents/audio/2012interviews/LS100197_mono.wav"
sound_channel = None     # the sound is in the left channel, set to None to disable extraction

# normalize transcript data in table
# these tuples of regexes and substitution strings will be 
# applied in order to each line of transcript
normalzn_rexs = [(re.compile(r"^(x[0-9]+|silence)$",re.I), ""),
                (re.compile(r"(（|\()(。|\.)(\)|）)|silence"), "{SL}"),
                (re.compile(r"。|\."), "{SL}"),
                (re.compile(r"(％|%)\s+((ha1 )+?|(he1 )+?)\s*(％|%)", re.I), "{LG}"),
                (re.compile(r"\[breath\]", re.I), "{BR}"),
                (re.compile(r"\[.+?\]|\#|\+|\^|\%|％|\-|\–|\～|\~|，|,|\:|：|？|\?"), ""),
                (re.compile("\xe3\x80\x80|\xef\xbc\x88|\xef\xbc\x8d|\xef\xbc\x89"), ""),
                (re.compile(r"(\S)\{"), "\\1 {"),
                (re.compile(r"\}(\S)"), "} \\1"),
                #(re.compile(r"(\w+)[1-5]"),"\\1"),     #remove the tone numbers
                (re.compile(r"([jqxy])[uü]", re.I), "\\1v"),
                (re.compile(r"([ln])ü", re.I), "\\1v")]
                
# load up that table!
table_file = open(table_filename)
table_elements = [[e.strip() for e in r.split('\t')] for r in table_file]
# clean up the text (6th column)
text_in = 5
for row_i in range(len(table_elements)):
    for re_i in range(len(normalzn_rexs)):
        table_elements[row_i][text_in] = normalzn_rexs[re_i][0].sub(normalzn_rexs[re_i][1], table_elements[row_i][text_in])
    table_elements[row_i][text_in] = table_elements[row_i][text_in].decode('utf-8').upper()  # is it only unicode because of that last regex??


# take anything not between {} and add it to a dictionary!        
have_to_be_in_it = """{BR}  br
{CG}  cg
{LG}  lg
{LS}  ls
{NS}  ns
{SL} sil
silence  sil
sp sp
!ENTER []
!EXIT []
"""

initial_re = re.compile(u'^[^AEIOUÜV]*',re.U)
final_re = re.compile(u'[AEIOUÜV].*(?=[1-5])',re.U)
controlseq_re = re.compile(r'\{.+\}')
words_list = [[w for w in r[text_in].split()] for r in table_elements]
words = set([word for sentence in words_list for word in sentence])
pinyin_dict = {}
dict_path = os.path.join(p2fa_path, 'model', 'dict')
# backup dict if it exists
if os.path.isfile(dict_path):
    # find a bkup locn
    backup_path = dict_path + '.bak'
    if os.path.isfile(backup_path):
        prefix = 1
        while os.path.isfile(backup_path):
            backup_path = dict_path + '.bak' + str(prefix)
            prefix = prefix + 1
    shutil.copy(dict_path, backup_path)
dict_file = codecs.open(dict_path, "w", 'utf-8')
#u_re = re.compile(r'(?<![LN])Ü'.decode('utf-8'))
#v_re = re.compile(r'(?<=[LN])Ü'.decode('utf-8'))
initials  = { 'C' :  'T S',
            'Z':     'D Z',
            'ZH':   'JH',
            'Q':     'CH',
            'X':     'SH',
            'J':     'JH',
            'H':     'HH'
            }
finals = {
    'A':	'AA1',
    'AI':	'AY1',
    'AO':	'AW1',
    'AN':	'AA1 N',
    'ANG':	'AA1 NG',

    'O':	'AO1',
    'ONG':	'OW1 NG',
    'OU':	'OW1',

    'E':	'AH1',
    'EI':	'EY1',
    'EN':	'AH1 N',
    'ENG':	'AH1 NG',
    'ER':	'ER1',

    'I':	'IY1',
    'IA':	'IY1 AA0',
    'IAN':	'IY1 EH0 N',
    'IAO':	'Y AW1',
    'IE':	'Y EH1',
    'IU':	'Y OW1',
    'IANG':	'Y AA1 NG',
    'IN':	'IH1 N',
    'ING':	'IH1 NG',
    'IONG':	'Y UH1 NG',

    'U':	'UW1',
    'UA':	'W AA1',
    'UO':	'W AO1',
    'UI':	'W EY1',
    'UAI':	'W AY1',
    'UAN':	'W AA1 N',
    'UN':	'W AH1 N',
    'UANG':	'W AA1 NG',

    u'V':	'IY1',
    u'VE':	'IY1 EY0',
    u'VAN':	'IY1 EH0 N',
    u'VN':	'IY1 AH0 N'}
for word in words:
    if controlseq_re.search(word) != None:
        continue
    print >> sys.stderr, "Word: ", word
    syl_initial = initial_re.findall(word)[0]
    syl_final = final_re.findall(word)[0]
    print >> sys.stderr, "Decomposition: ", syl_initial, ', ', syl_final
    
    # create a pronunciation for it! we have rules.
    # TODO: add <I> difference for shi/xi
    # TODO: YI/YIN pronunciations broken
    syl_pronunciation=initials.get(syl_initial,syl_initial) + " " + finals.get(syl_final)
    #syl_pronunciation = "B AE1 M"
    #word = v_re.sub('V', u_re.sub('V',word))

    pinyin_dict[word] = syl_pronunciation
    dict_file.write(word + '  ' + syl_pronunciation + '\n')
dict_file.write(have_to_be_in_it)
dict_file.close()

# now the alignment part!
# loop through each row of the table and perform an alignment
#temp_wav_name = "temp.wav"
temp_trs_name = "temp.txt"
textgrid_decorator = 1
num_failed = -1
time_to_wait = 0.05
failed_rows = []
# TODO: have it wait when you fail, and try again
while num_failed != 0 and time_to_wait < 15:
    num_failed = 0
    failed_rows = []
    for table_row in table_elements:
        if table_row[text_in] != "":
            textgrid_name = "textgrid" + str(textgrid_decorator) + ".textgrid"
            print >> sys.stderr, "Aligning "+ str(textgrid_decorator) + ": " + table_row[text_in]

            # try aligning it!
            start_time = float(table_row[2]) / 1000
            end_time = float(table_row[3]) / 1000
            
            # now align
            try:
                temp_trs = codecs.open(temp_trs_name, "w", "utf-8")
                temp_trs.write(table_row[text_in])
                temp_trs.close()
                result_code = subprocess.call(['python', os.path.join(p2fa_path, "align.py"), 
                    '-s ' + str(start_time), '-e ' + str(end_time), sound_path, temp_trs_name, textgrid_name])
                if result_code != 0:
                    raise IOError("Alignment failed")
                # delete the intermediate files
                #os.remove(temp_wav_name)
                os.remove(temp_trs_name)
                time.sleep(time_to_wait)
            except IOError as e:
                print >> sys.stderr, "Failed on this row***********"
                print >> sys.stderr, str(e)
                num_failed = num_failed + 1
                failed_rows.append(table_row)
            finally:
                textgrid_decorator = textgrid_decorator + 1
    time_to_wait = time_to_wait * 1.5
    table_elements = failed_rows        # destructive, watch out
    if num_failed > 0:
        print >> sys.stderr, num_failed, " failed rows, restarting"
        time.sleep(3)
        print >> sys.stderr, failed_rows
   