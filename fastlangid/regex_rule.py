import os
import re


UNICODE_MAPPING_FILE = os.path.join(os.path.dirname(__file__), 'models', 'unicode_lang.dict')

def convert2unicode(code):
    code_list = code.split('-')
    output_code = []
    for _unicode in code_list:
        if 'U+' in _unicode:
            code = _unicode.split('U+')[1]
            code = '0'*(4-len(code))+code
            _unicode = fr'\u{code}'
        output_code.append(_unicode)
    return '-'.join(output_code)


def init_dict():
    language2regex_list = {}
    with open(UNICODE_MAPPING_FILE, 'r') as f:
        for line in f:
            data = line.rstrip()
            tokens = data.split('\t')
            unicode, languages = tokens[0], tokens[1:]
            for lang in languages:
                if lang not in language2regex_list:
                    language2regex_list[lang] = []
                language2regex_list[lang].append(convert2unicode(unicode))

    lang_regex = {}
    for lang, regex_block in language2regex_list.items():
        lang_regex[lang] = re.compile('[{}]'.format('|'.join(regex_block)))

    return lang_regex


lang2regex = init_dict()

def find_matched_language(text):
    matched_lang = []
    text_len = len(text)
    if text_len == 0:
        return matched_lang

    matched_fast = []
    for lang, char_reg in lang2regex.items():
        if char_reg.search(text) is not None:
            matched_char = len(list(re.finditer(char_reg, text)))
            fast_lang = lang
            if lang[:2] == 'zh':
                fast_lang = 'zh'
            matched_lang.append((lang,  matched_char/ text_len, fast_lang ))

    if len(matched_lang) == 0:
        return matched_lang

    return sorted(matched_lang, key= lambda x:x[1], reverse=True)
