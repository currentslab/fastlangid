# coding=utf-8
from __future__ import division, unicode_literals
from fastlangid.langid import LID
from os import path
import unittest





class FastLangIdTest(unittest.TestCase):

    def setUp(self):
        self.langid = LID()

    def test_model_present(self):
        self.assertEqual(path.isfile(self.langid.model_file), True)
        self.assertEqual(path.isfile(self.langid.sup_model_file), True)

    def test_single_prediction(self):

        lang_code = self.langid.predict('這是繁體字')
        self.assertEqual(lang_code, 'zh-hant' )

        lang_code = self.langid.predict('简体中文')
        self.assertEqual(lang_code, 'zh-hans' )

        lang_code = self.langid.predict('이것은 한국인입니다')
        self.assertEqual(lang_code, 'ko' )

    def test_list_probs(self):
        lang_codes = self.langid.predict('這是繁體字', prob=True, k=5)
        self.assertTrue(isinstance(lang_codes,  list))
        self.assertEqual(lang_codes[0][0], 'zh-hant' )

        lang_codes = self.langid.predict('the brown fox jumps over the lazy dog', prob=True, k=5)
        self.assertTrue(isinstance(lang_codes,  list))
        self.assertEqual(lang_codes[0][0], 'en' )

    def test_for_equality(self):

        for name in ['小美', '小明', '老王','阿公', '陳美珍']:
            lang_code = self.langid.predict('{}決定要去購買新的項鍊'.format(name))
            self.assertEqual(lang_code, 'zh-hant' )

        for name in ['小美', '小明', '老王','阿公', '陈美珍']:
            lang_code = self.langid.predict('{}决定要去购买新的项链'.format(name))
            self.assertEqual(lang_code, 'zh-hans' )


        for name in ['Peter', 'Dmitri', 'Jonas','Rahul', 'Mohamed', 'Ali']:
            lang_code = self.langid.predict('{} is going to London this week'.format(name))
            self.assertEqual(lang_code, 'en' )


    def test_edge_cases(self):
        # brand in test case sentences are fictional and created only for testing purposes

        lang_code = self.langid.predict('2K 也決定從 NZIDIA GeForze Then 平台撤出')
        self.assertEqual(lang_code, 'zh-hant' )

        lang_code = self.langid.predict('GTC推出VIVE Synz AR虛擬會議服務,攜中X電信完成三地AR會議')
        self.assertEqual(lang_code, 'zh-hant' )

        lang_code = self.langid.predict('XuaWEI真無線藍牙降噪耳機、穿戴新品齊發,XUAWEI FreeBeds 3搭配XUAWEI WATCH CT2加碼限定好禮!')
        self.assertEqual(lang_code, 'zh-hant' )

        lang_code = self.langid.predict('平嘢有冇好嘢?~$500真無線耳機評測 Sabbot K12 Ultra | Edofier TZS 5 | Soeul ST-XX | 米Air 2 【Market.test.tw產品比較】')
        self.assertEqual(lang_code, 'zh-hant' )

        lang_code = self.langid.predict('沈鸣人:OPO Fid Z2系列缎黑等配色会逐渐补货,开售当日会加货')
        self.assertEqual(lang_code, 'zh-hans' )

        lang_code = self.langid.predict('平嘢有冇好嘢?', force_second=True)
        self.assertEqual(lang_code, 'zh-yue' )

        lang_code = self.langid.predict('iPhone 7成功刷入Android 10 蘋果控告技術擁有公司')
        self.assertEqual(lang_code, 'zh-hant' )

    
    def test_batches(self):
        lang_codes = self.langid.predict(['iPhone 7成功刷入Android 10 蘋果控告技術擁有公司', 
            'РФ и еще 26 стран назовут своих представителей на "Евровидении" до 9 марта',
            'BroadcomAktie Aktuell  Broadcom notiert mit 3 Prozent deutliche Verluste', 
            'the brown fox jumps over the lazy dog',
            'Pokémon Spada e Scudo: rivelato il nuovo Pokémon misterioso Zarude',
            'Vidéo : Amazon ouvre un supermarché alimentaire sans caisse',
            '英国:6月でEUとの交渉終了も辞さない構え、離脱後の通商協定巡り - Bloomberg',
            'Braga garante internacional português',
            ])
        self.assertEqual(lang_codes,  ['zh-hant', 'ru', 'de', 'en','it', 'fr', 'ja', 'pt'])




def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(FastLangIdTest))
    return suite


if __name__ == '__main__':
    unittest.main()