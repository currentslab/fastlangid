import fasttext
import re

model = fasttext.load_model('fastlangid/models/lid.176.ftz')

def _clean_up(txt):
    txt = re.sub(r"\b\d+\b", "", txt)
    return txt
print("These examples should equal to zh, however example 3,4,5 is equal to ja")
# These examples should equal to zh, however example 3,4,5 is equal to ja
# 1.
print(model.predict(_clean_up("2K 也決定從 NVIDIA GeForce Now 平台撤出")), '== zh')
# 2.
print(model.predict(_clean_up("HTC推出VIVE Sync VR虛擬會議服務,攜中華電信完成三地VR會議")), '== zh')
# 3.
print(model.predict(_clean_up("HUAWEI真無線藍牙降噪耳機、穿戴新品齊發,HUAWEI FreeBuds 3搭配HUAWEI WATCH GT2加碼限定好禮!")), '== zh')
# 4.
print(model.predict(_clean_up("平嘢有冇好嘢?~$500真無線耳機評測 Sabbat E12 Ultra | Edifier TWS 5 | Soul ST-XX | 小米Air 2 【Price.com.hk產品比較】")), '== zh')
# 5.
print(model.predict(_clean_up("沈义人:OPPO Find X2系列缎黑等配色会逐渐补货,开售当日会加货")), '== zh')
# 6.
print(model.predict(_clean_up("iPhone 7成功刷入Android 10 蘋果控告技術擁有公司")), '== zh')

print("Cascade Fasttext model")

from fastlangid.langid import LID
model = LID()
# These examples should equal to zh, however example 3,4,5 is equal to ja
# 1.
print(model.predict(_clean_up("2K 也決定從 NVIDIA GeForce Now 平台撤出")), '== zh-hant')
# 2.
print(model.predict(_clean_up("HTC推出VIVE Sync VR虛擬會議服務,攜中華電信完成三地VR會議")), '== zh-hant')
# 3.
print(model.predict(_clean_up("HUAWEI真無線藍牙降噪耳機、穿戴新品齊發,HUAWEI FreeBuds 3搭配HUAWEI WATCH GT2加碼限定好禮!")), '== zh-hant')
# 4.
print(model.predict(_clean_up("平嘢有冇好嘢?~$500真無線耳機評測 Sabbat E12 Ultra | Edifier TWS 5 | Soul ST-XX | 小米Air 2 【Price.com.hk產品比較】")), '== zh-hant')
# 5.
print(model.predict(_clean_up("沈义人:OPPO Find X2系列缎黑等配色会逐渐补货,开售当日会加货")), '== zh-hans')
# 6.
print(model.predict(_clean_up("iPhone 7成功刷入Android 10 蘋果控告技術擁有公司")), '== zh-hant')
