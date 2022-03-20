from __future__ import division, unicode_literals

import re
import os, sys, contextlib
import collections
from fasttext import load_model
import fasttext
from fastlangid.utils import (
    clean_text,
    only_punctuations,
    input_preprocess,
    UNCERTAIN_SETS,
    UNK_CLS,
    REGEX_NOT_SUPPORT,
    CHINESE_FAMILY_CODES
)
from fastlangid.regex_rule import find_matched_language


fasttext.FastText.eprint = lambda x: None
if sys.version_info[0] >= 3:
    unicode = str


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

    def _second_stage(self, text, k, prob, filter_only_han_char=False):
        labels_, probs_ = self.sup_model.predict(text, k=k)

        lang_ids = list(map(lambda x: x.replace("__label__", ""), labels_))
        if filter_only_han_char:
            results = [ (lang_id, probs_[idx]  ) for idx, lang_id in enumerate(lang_ids) if lang_id in CHINESE_FAMILY_CODES]
        else:
            results = list(zip(lang_ids, probs_))
        if prob: # validate prob is not None
            return results
        return [r[0] for r in results ] if k > 1 else results[0][0]

    def _predict_text(self, text, supplement_threshold=0.93, k=1, prob=False, force_second=False):
        matched_lang = find_matched_language(text)

        fastlang_code = set([ m[2] for m in matched_lang])
        if fastlang_code == UNCERTAIN_SETS:
            # regex match only found uncertain sets : zh, ko, ja
            # we will skip first stage model
            return self._second_stage(text, k, prob)

        k = max(1, k)

        labels, probs = self.model.predict(text, k=10)
        lang_ids = list(map(lambda x: x.replace("__label__", ""), labels))


        # fasttext models usually confuse chinese, korean, japanese words
        # if the model is not so sure we pass to our model to reduce down the uncertainty
        if lang_ids[0] in UNCERTAIN_SETS and ((probs[0] < supplement_threshold) or force_second):
            return self._second_stage(text, k, prob)
        # predict chinese: now we want to know what language is it
        elif (lang_ids[0] == 'zh' and probs[0] >= supplement_threshold) or force_second:
            return self._second_stage(text, k, prob, filter_only_han_char=True)
        
        valid_langs = []
        valid_lang_ids = []

        for lang_id, p in zip(lang_ids, probs):
            if lang_id in fastlang_code or lang_id in REGEX_NOT_SUPPORT:
                valid_langs.append((lang_id, p))
                valid_lang_ids.append(lang_id)

        # return list of predictions
        if prob:
            return  valid_langs[:k] if k > 1 else valid_langs[0]
        return valid_lang_ids[:k] if k > 1 else valid_lang_ids[0]

    def clean_up(self, text, full_clean=False):
        if full_clean:
            text = clean_text(text)
        return input_preprocess(text)

    def predict(self, text, full_clean=False,supplement_threshold=0.9, k=1, prob=False, force_second=False ):
        if isinstance(text, unicode):
            text = self.clean_up(text, full_clean=full_clean)
            if len(text) == 0:
                return UNK_CLS
            elif only_punctuations(text):
                return UNK_CLS

            return self._predict_text(text, supplement_threshold=supplement_threshold, k=k, prob=prob, force_second=force_second)
        else:
            batch = [ self.clean_up(i, full_clean=full_clean) for i in text ]
            return [ self._predict_text(b, supplement_threshold=supplement_threshold, k=k, prob=prob, force_second=force_second) for b in batch ]
