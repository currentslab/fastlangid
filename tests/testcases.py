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


    def test_top_k(self):

        for name in ['Peter', 'Dmitri', 'Jonas','Rahul', 'Mohamed', 'Ali']:
            lang_code = self.langid.predict('{} is going to London this week'.format(name), k=5)
            self.assertEqual(len(lang_code), 5)
        for name in ['Peter', 'Dmitri', 'Jonas','Rahul', 'Mohamed', 'Ali']:
            lang_code = self.langid.predict('{} is going to London this week'.format(name), k=5, prob=True)
            self.assertEqual(len(lang_code), 5)

        for name in ['Peter', 'Dmitri', 'Jonas','Rahul', 'Mohamed', 'Ali']:
            lang_code_w_prob = self.langid.predict('{} is going to London this week'.format(name), k=1, prob=True)
            lang_code, prob = lang_code_w_prob
            self.assertEqual(len(lang_code_w_prob), 2)
            self.assertEqual(lang_code, 'en')


    def failed_test_case(self):
        sentences = [
            '人為過度捕獵 鯊魚數量減少70%',
            'The Fierce Vulnerability of DMX',
            'M1 iPad Pro在台開賣！11吋台幣24900元起、12.9吋Mini LED款台幣34900元起',
            '《KDOQI慢性肾脏病营养实践指南2020更新版》专家谈',
            '宜蘭東門夜市砍人案起因是她　3高中生險遭誤砍！警快打逮1嫌 | ETtoday社會新聞',
            'IG收私訊「兼職日進千元」私訊　男大生匯款遭「總裁」詐騙 ｜ 蘋果新聞網 ｜ 蘋果日報',
            'LDH: COVID-19 cases total 380K',
            '【專欄】台積電來美設廠是榮耀也是義務',
            'wwe-fastlane-live-stream-free-watch-online',
            'HBL／嘉中羅楷翔文武雙全 乙級尋夢',
            'RTX 3080 Ti 12GB傳將四月報到、RTX 3070 Ti 8GB則五月跟上'
        ]
        for sent in sentences:
            lang_code = self.langid.predict(sent, prob=True, k=10)
            self.assertEqual(lang_code, 'zh-hant' )


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