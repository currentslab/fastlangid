from __future__ import division, unicode_literals

import re
import os, sys, contextlib
import collections
from fasttext import load_model
import fasttext

if sys.version_info[0] >= 3:
    unicode = str


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
    results = re.sub(HTML_CLEANER, "", results)

    results = re.sub(RAW_CONTENT_CLEANER, "", str(text))
    results = results.strip()
    for regex_match, replace_token in WHITE_SPACE_CLEANER:
        results = re.sub(regex_match, replace_token, results)
    return results


MODEL_FILE = os.path.join(os.path.dirname(__file__), 'models', 'lid.176.ftz')
SUPPLEMENT_MODLE_FILE = os.path.join(os.path.dirname(__file__), 'models', 'model_s.ftz')

class LID():
    def __init__(self, custom_model=None, sup_custom_model=None):
        self.model_file = MODEL_FILE
        if custom_model is not None:
            self.model_file = custom_model
            if not os.path.exists(custom_model):
                raise OSError('Custom model path not found at '+ str(custom_model))

        self.sup_model_file = SUPPLEMENT_MODLE_FILE
        if sup_custom_model is not None:
            self.sup_model_file = sup_custom_model
            if not os.path.exists(sup_custom_model):
                raise OSError('Custom supplement model path not found at ' + str(sup_custom_model))
        fasttext.FastText.eprint = print

        with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
            self.sup_model = load_model(self.sup_model_file)
            self.model = load_model(self.model_file)


    def _predict_text(self, text, supplement_threshold=0.93, k=1, prob=False, force_second=False):
        k = min(1, k)
        labels, probs = self.model.predict(text, k=k)
        lang_ids = list(map(lambda x: x.replace("__label__", ""), labels))
    
        if lang_ids[0] in ['ko', 'zh', 'ja'] and ((probs[0] < supplement_threshold) or force_second):
            labels_, probs_ = self.sup_model.predict(text, k=k)
            lang_ids = list(map(lambda x: x.replace("__label__", ""), labels_))
            results = list(zip(lang_ids, probs_))
            if prob:
                return list(zip(lang_ids, probs_))
            return lang_ids[0]
        elif (lang_ids[0] == 'zh' and probs[0] >= supplement_threshold) or force_second:
            labels_, probs_ = self.sup_model.predict(text, k=4)
            lang_ids = list(map(lambda x: x.replace("__label__", ""), labels_))

            results = [ (lang_id, probs_[idx]  ) for idx, lang_id in enumerate(lang_ids) if lang_id in ['zh-hant', 'zh-hans'] ]
            results.sort(key=lambda x: x[1], reverse=True)
            if prob: # validate prob is not None
                return results
            return results[0][0]

        # return list of predictions
        if prob:
            return list(zip(lang_ids, probs_))
        return lang_ids[0]

    def clean_up(self, text, full_clean=False):
        if full_clean:
            text = clean_text(text)
        return input_preprocess(text)

    def predict(self, text, full_clean=False,supplement_threshold=0.9, k=1, prob=False, force_second=False ):
        if isinstance(text, unicode):
            text = self.clean_up(text, full_clean=full_clean)
            if len(text) == 0:
                raise ValueError("input text is not sufficient")
            return self._predict_text(text,supplement_threshold=supplement_threshold, k=k, prob=prob, force_second=force_second)
        else:
            batch = [ self.clean_up(i, full_clean=full_clean) for i in text ]
            return [ self._predict_text(b, supplement_threshold=supplement_threshold, k=k, prob=prob, force_second=force_second) for b in batch ]
