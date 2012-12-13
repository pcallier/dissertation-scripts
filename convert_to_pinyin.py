#!/usr/bin/python
# coding=utf-8
 
# going to use this tool: http://www.purpleculture.net/chinese-pinyin-converter/
# how to use: POST with a form, see below.

# Let's try it!
import urllib,urllib2,re,string,sys, time

class ConversionFailure(Exception):
    None
 
class NoHanCharacters(Exception):
    None
    
def get_conversion_result(to_convert,wait_time=0.5): 
    # first test the string to make sure it has Han characters in it
    #any_han_yet = False
    if re.search(u'[\u4e00-\u9eff]', to_convert.decode('utf-8')) == None:
        #print >> sys.stderr, "Skipping the internet..."
        raise NoHanCharacters
    
    converter_url = "http://www.purpleculture.net/chinese-pinyin-converter/"
    conv_option = "number"
    if wait_time > 10:
        raise ConversionFailure
    
    # New converter, with two options
    # wdqchs:e.g.,中庸之道
    # tone:number
    
    # build request object
    my_post_data = urllib.urlencode({"wdqchs":to_convert,
                                    "tone": conv_option})
    my_request = urllib2.Request(converter_url, my_post_data)

    try:
        request_result = urllib2.urlopen(my_request)
    except urllib2.HTTPError as e:
        print >> sys.stderr, "Error " + str(e)
        print >> sys.stderr, "Waiting " + wait_time * 1000 + ' ms'
        time.sleep(wait_time)
        wait_time = wait_time * 1.8
        return get_conversion_result(to_convert, wait_time)
        
    return(request_result)
    
def extract_pinyin(request_result):
    result_lines = request_result.readlines()
    # get the pinyin out of it
    # our pinyin regex looks like this:
    pinyin_re = re.compile(r'^.*result = "(.*)";.*$')
    pinyin_final_space_re = re.compile(r' $')       # this is for culling the annoying final space
                                                    # introduced by the pinyin converter, which 
                                                    # the program ends up interpreting as a missing
                                                    # element
    chinese_re = re.compile(r'^.*ori_cn += +"(.*)";.*$')
                                                    
    # find the pinyin
    for result_line in result_lines:
        result_match = pinyin_re.match(result_line)
        if result_match != None:
            the_pinyin = pinyin_final_space_re.sub('', result_match.groups()[0])
            break
    # find the chinese        
    for result_line in result_lines:
        #if result_line.find("ori_cn") != -1:
            #print >> sys.stderr, result_line
        result_match = chinese_re.match(result_line)
        if result_match != None:
            original_chinese = result_match.groups()[0]
            #print >> sys.stderr, "HIT!"
            break        
    
    # now, we need to parse through the results and add back in characters
    # the converter left out
    # the pinyin data has *extra* spaces to show where stuff got left out
    pinyin_tokens = the_pinyin.split(" ")
    # this has ' ' for missing elements now.  missing elements are one-char-by-one
    
    original_tokens = list(original_chinese.decode('utf-8'))
    #print >> sys.stderr, "The pinyin: ", the_pinyin
    #print >> sys.stderr, pinyin_tokens
    #print >> sys.stderr, original_tokens
    pinyin_result = ""
    assert len(pinyin_tokens) == len(original_tokens)
    # need to keep track of what kind of token we last put on
    # in order to keep track of whitespace
    # probably a less fragile way of doing this exists
    TT_START = 0
    TT_PINSYL = 1
    TT_OTHERTOKEN = 2
    TT_WHITESPACE = 3
    last_token_type = TT_START
    for token_i in range(0,len(pinyin_tokens)):
        if pinyin_tokens[token_i] == "":
            if original_tokens[token_i] in (' ','\t'):
                last_token_type = TT_WHITESPACE
            else:
                last_token_type = TT_OTHERTOKEN
            pinyin_result = pinyin_result + original_tokens[token_i]
        else:
            py_suffix = " "
            # add a space before pinyin if last token was not pinyin or whitespace or beginning
            if last_token_type == TT_OTHERTOKEN:
                py_prefix = " "
            else:
                py_prefix = ""
            
            pinyin_result = pinyin_result + py_prefix + pinyin_tokens[token_i] + py_suffix
            last_token_type = TT_PINSYL

    return(pinyin_result.strip())

to_convert = sys.argv[1].strip()
try:
    conversion_result = get_conversion_result(to_convert)
except NoHanCharacters:
    pinyin = to_convert
    print (pinyin.decode('utf-8'))
    sys.exit()
    
pinyin = extract_pinyin(conversion_result)
print (pinyin.encode('utf-8'))

