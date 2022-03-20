# coding=utf-8
from __future__ import division, unicode_literals
from os import path
import unittest

from fastlangid.regex_rule import find_matched_language
from fastlangid.langid import LID


ZH_HANS = "分词就是将连续的字序列按照一定的规范重新组合成语义独立词序列的过程。"
ZH_HANT = "分詞就是將連續的字序列按照一定的規範重新組合成詞語獨立的次序過程。"
KO = "단어 분할은 연속적인 단어 시퀀스를 특정 사양에 따라 의미적으로 독립적인 단어 시퀀스로 재결합하는 프로세스입니다."
JA = "単語のセグメンテーションは、特定の仕様に従って、連続する単語シーケンスを意味的に独立した単語シーケンスに再結合するプロセスです。"
DE = "Deutsches Ipsum Dolor id latine Stuttgart complectitur pri, mea meliore denique Die Toten Hosen id. Elitr expetenda nam an, was machst du ei reque euismod assentior. Odio Autobahn iracundia ex pri. Ut vel bitte mandamus, quas natum adversarium ei Juttensack diam minim honestatis eum no"

FA = "اوانز تو فقط يک هفته وقت داري وگرنه خونتو خواهيم سوزوند ."
UG = "ھەممە ئادەم تۇغۇلۇشىدىنلا ئەركىن، ئىززەت۔ھۆرمەت ۋە ھوقۇقتا باب۔باراۋەر بولۇپ تۇغۇلغان. ئۇلار ئەقىلگە ۋە ۋىجدانغا ئىگە ھەمدە بىر۔بىرىگە قېرىنداشلىق مۇناسىۋىتىگە خاس روھ بىلەن مۇئامىلە قىلىشى كېرەك.‎"

class RegexTest(unittest.TestCase):

    def test_format(self):
        output = find_matched_language(ZH_HANS)   
        self.assertEqual(len(output) > 0, True)
        self.assertEqual(len(output[0]) == 3, True)
    
    def test_results(self):
        output = find_matched_language(ZH_HANS)
        encodings = [o[2]  for o in output ]
        self.assertTrue( 'zh' in encodings )
        encodings = [o[0]  for o in output ]
        self.assertTrue( 'zh-hans' in encodings )


        output = find_matched_language(ZH_HANT)
        encodings = [o[2]  for o in output ]
        self.assertTrue( 'zh' in encodings )
        encodings = [o[0]  for o in output ]
        self.assertTrue( 'zh-hant' in encodings )

        output = find_matched_language(KO)
        encodings = [o[2]  for o in output ]
        self.assertTrue( 'ko' in encodings )
        encodings = [o[0]  for o in output ]
        self.assertTrue( 'ko' in encodings )

        output = find_matched_language(JA)
        encodings = [o[2]  for o in output ]
        self.assertTrue( 'ja' in encodings )
        encodings = [o[0]  for o in output ]
        self.assertTrue( 'ja' in encodings )

        output = find_matched_language(DE)
        encodings = [o[2]  for o in output ]
        self.assertTrue( 'de' in encodings )
        encodings = [o[0]  for o in output ]
        self.assertTrue( 'de' in encodings )

    def test_regex_not_supported(self):
        '''
            Ensure languages which is not supported in regex list
            are still output from fasttext
        '''
        # urgu language is not inside regex chars
        langid = LID()

        self.assertTrue( langid.predict(UG) == 'ug' )
        output = langid.predict(UG, k=5, prob=True)
        self.assertTrue('ug' in [o[0] for o in output])
        self.assertTrue('ug' in langid.predict(UG, k=5, prob=False))

        self.assertTrue( langid.predict(FA) == 'fa' )
        output = langid.predict(FA, k=5, prob=True)
        self.assertTrue('fa' in [o[0] for o in output])
        self.assertTrue('fa' in langid.predict(FA, k=5, prob=False))



