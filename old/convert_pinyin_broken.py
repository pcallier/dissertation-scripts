def get_conversion_result(to_convert): 
    converter_url = "http://www.words-chinese.com/pinyin-converter/"
    conv_option = "pinyin_all"
    lang_option = "english"

    # build request object
    my_post_data = urllib.urlencode({"text":to_convert,
                                    "conv": conv_option,
                                    "lang": lang_option})
    my_request = urllib2.Request(converter_url, my_post_data)

    request_result = urllib2.urlopen(my_request)
    return(request_result)

def extract_pinyin(request_result):
    result_lines = request_result.readlines()
    # get the pinyin out of it
    # our pinyin regex looks like this:
    pinyin_re = re.compile(r"^.*?Convert to pinyin:.*?\<\/pre\>(.*?)\<\/pre\>.*?$")
    for result_line in result_lines:
        result_match = pinyin_re.match(result_line)
        if result_match != None:
            return(result_match.groups()[0])
    
    
def maketransU(s1, s2, todel=""):
    # from http://bytes.com/topic/python/answers/520355-string-translate-unicode
    trans_tab = dict( zip( map(ord, s1), map(ord, s2) ) )
    trans_tab.update( (ord(c),None) for c in todel )
    return trans_tab            
  
def clean_up_pinyin(to_clean_up):
    """
    Clean up results from the original (bad) conversion fn
    """
    pinyin_version = extract_pinyin(conversion_result).strip()
    # now how to convert those pesky diacritic-laden results to ASCII
    # this is missing cap U, V, I, but we shouldn't have caps anyway
    input_chars =  u"?á?à?ó?ò?é?è?í?ì?ú?ù????ü?Á?À?Ó?Ò?É?È"
    output_chars = u"aaaaooooeeeeiiiiuuuuüüüüüAAAAOOOOEEEE"
    pinyin_translation_table = maketransU(input_chars,output_chars)
    translated_pinyin = pinyin_version.decode('utf-8').translate(pinyin_translation_table)

    # clean up the result
    import HTMLParser
    h = HTMLParser.HTMLParser()
    unescaped_translated_pinyin = h.unescape(translated_pinyin)
    # replace \xa0
    unescaped_translated_pinyin = unescaped_translated_pinyin.replace(u'\xa0', u' ')
    # normalize whitespace
    clean_pinyin = re.sub(r"\s+", " ", unescaped_translated_pinyin)

    return(clean_pinyin)