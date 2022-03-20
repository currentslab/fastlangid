import re
import os

symbol_removal = re.compile(r"[.\!?,'/()。，，；:\–‘\-\[\]【】|~、…「」“”《》=——+～！@#$%⋯⋯&*（）\n\t]")
RAW_CONTENT_CLEANER = re.compile(r"#video_container #my-video{width:100%;padding-bottom:56.25%; height:56.25%;}|\[embedded content\]|Newsfrom Japan")
WHITE_SPACE_CLEANER = [
	(re.compile(r"\s\s+"), " "),
	(re.compile(r"\n+"), "\n\n"),
	(re.compile(r"\t+"), "\t\t"),
]
HTML_CLEANER = re.compile(r'<.*?>')

def input_preprocess(text):
    text = re.sub(symbol_removal, "", text.strip())
    # text = text.replace('Yahoo', '')
    return text

def clean_text(text):

    results = re.sub(RAW_CONTENT_CLEANER, "", str(text))
    results = re.sub(HTML_CLEANER, "", results)
    results = results.strip()
    for regex_match, replace_token in WHITE_SPACE_CLEANER:
        results = re.sub(regex_match, replace_token, results)
    return results

UNK_CLS = '<unk>'

with open(os.path.join(os.path.dirname(__file__), 'models', 'punc.dict'), 'r', encoding='utf-8') as f:
    PUNCTUATION = set(list(f.read().strip()))

def only_punctuations(text):
    for char in set(text):
        if char not in PUNCTUATION:
            return False
    return True

UNCERTAIN_SETS = set(('zh', 'ko', 'ja'))

CHINESE_FAMILY_CODES =  set(('zh-hant', 'zh-hans', 'zh-yue'))


REGEX_NOT_SUPPORT = set(['als',
 'am',
 'an',
 'arz',
 'as',
 'ast',
 'av',
 'az',
 'azb',
 'ba',
 'bar',
 'bcl',
 'bh',
 'bn',
 'bo',
 'bpy',
 'br',
 'bs',
 'bxr',
 'ca',
 'cbk',
 'ce',
 'ceb',
 'ckb',
 'co',
 'cv',
 'cy',
 'da',
 'diq',
 'dsb',
 'dty',
 'dv',
 'eml',
 'eu',
 'fa',
 'frr',
 'fy',
 'gd',
 'gl',
 'gn',
 'gom',
 'gv',
 'hif',
 'hsb',
 'ht',
 'hy',
 'ia',
 'ie',
 'ilo',
 'io',
 'jbo',
 'jv',
 'ka',
 'km',
 'kn',
 'krc',
 'ku',
 'kv',
 'kw',
 'la',
 'lb',
 'lez',
 'li',
 'lmo',
 'lo',
 'lrc',
 'lv',
 'mai',
 'mg',
 'mhr',
 'min',
 'ml',
 'mr',
 'mrj',
 'mwl',
 'my',
 'myv',
 'mzn',
 'nah',
 'nap',
 'nds',
 'ne',
 'new',
 'nn',
 'no',
 'oc',
 'or',
 'os',
 'pa',
 'pam',
 'pfl',
 'pms',
 'pnb',
 'qu',
 'rm',
 'rue',
 'sa',
 'sah',
 'sc',
 'scn',
 'sco',
 'sd',
 'sh',
 'si',
 'sl',
 'so',
 'sq',
 'su',
 'tg',
 'tl',
 'tt',
 'tyv',
 'ug',
 'vec',
 'vep',
 'vls',
 'vo',
 'wa',
 'war',
 'wuu',
 'xal',
 'xmf',
 'yi',
 'yo',
 'yue'])