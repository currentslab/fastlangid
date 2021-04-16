# fastlangid

[![codecov](https://codecov.io/gh/currentsapi/fastlangid/branch/master/graph/badge.svg)](https://codecov.io/gh/currentsapi/fastlangid)  [![PyPI version](https://badge.fury.io/py/fastlangid.svg)](https://badge.fury.io/py/fastlangid)


Language identification that includes traditional and simplified Chinese.


## Why and who is this package for?

This is a language identification language focus on providing higher accuracy in Japanese, Korean, and Chinese language compares to the original Fasttext model ( lid.176.ftz ). This package also include identification for simplified and traditional Chinese language.


|         Model         |  F1@1  |
|-----------------------|--------|
| lid.176.ftz           | 0.977  |

We can achieve higher accuracy by including an additional language identification model to handle low confidence scores for Japanese, Korean, Chinese. The table below shows F1 (k=1) scores in identifying 3 languages. (we updated the validation corpus which is much harder to the first revision : shorter text, latest news text )


|   2nd-Stage Model     |  F1@1  |  Acc@1  |
|-----------------------|--------|--------|
| version 1.0.0         | 0.826  | 0.744  |
| master                | 0.801  | 0.894  |

Master version is also trained with identifying Cantonese (zh-yue) text from Mozilla Common Voice corpus text. Currently the model is senstive to non cantonese text mixing inside the sentence, hence please use the model with care.

To use Cantonese prediction, it recommended to force inference using the second stage prediction

```
lang_code = langid.predict('平嘢有冇好嘢?', force_second=True)
```


For more edge case detail please refer to [fasttext_issues.py](tests/fasttext_issues.py)


The training data for the supplement model was drawn from Common Crawl Corpus and [Currents API](https://currentsapi.services/en) internal language dataset.

We wish to support Cantonese language in the upcoming future. Feel free to contact us if you would like to provide any related corpus.


## Install


```bash
$ pip install fastlangid
```

## Example

Only one function call away to handle single or multiple sentences

```
from fastlangid.langid import LID
langid = LID()
result = langid.predict('This is a test')
print(result)
```


```
from fastlangid.langid import LID
langid = LID()
examples = [
  '中文繁體',
  '中文简体',
  'Lorem Ipsum is simply dummy text of the printing and typesetting industry',
  'Lorem Ipsum adalah text contoh digunakan didalam industri pencetakan dan typesetting',
  'Le Lorem Ipsum est simplement du faux texte employé dans la composition et la mise en page avant impression'
]
results = langid.predict(examples)
print(results)
```



## Supported Languages

Supports 177 languages. The ISO codes for the corresponding languages are as below.

```
af als am an ar arz as ast av az azb ba bar bcl be bg bh bn bo bpy br bs bxr ca cbk
ce ceb ckb co cs cv cy da de diq dsb dty dv el eml en eo es et eu fa fi fr frr fy ga
gd gl gn gom gu gv he hi hif hr hsb ht hu hy ia id ie ilo io is it ja jbo jv ka kk km
kn ko krc ku kv kw ky la lb lez li lmo lo lrc lt lv mai mg mhr min mk ml mn mr mrj ms
mt mwl my myv mzn nah nap nds ne new nl nn no oc or os pa pam pfl pl pms pnb ps pt qu
rm ro ru rue sa sah sc scn sco sd sh si sk sl so sq sr su sv sw ta te tg th tk tl tr
tt tyv ug uk ur uz vec vep vi vls vo wa war wuu xal xmf yi yo yue zh-hans zh-hant
```

## Reference

### Enriching Word Vectors with Subword Information

[1] P. Bojanowski\*, E. Grave\*, A. Joulin, T. Mikolov, [*Enriching Word Vectors with Subword Information*](https://arxiv.org/abs/1607.04606)

```
@article{bojanowski2016enriching,
  title={Enriching Word Vectors with Subword Information},
  author={Bojanowski, Piotr and Grave, Edouard and Joulin, Armand and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1607.04606},
  year={2016}
}
```

### Bag of Tricks for Efficient Text Classification

[2] A. Joulin, E. Grave, P. Bojanowski, T. Mikolov, [*Bag of Tricks for Efficient Text Classification*](https://arxiv.org/abs/1607.01759)

```
@article{joulin2016bag,
  title={Bag of Tricks for Efficient Text Classification},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1607.01759},
  year={2016}
}
```

### FastText.zip: Compressing text classification models

[3] A. Joulin, E. Grave, P. Bojanowski, M. Douze, H. Jégou, T. Mikolov, [*FastText.zip: Compressing text classification models*](https://arxiv.org/abs/1612.03651)

```
@article{joulin2016fasttext,
  title={FastText.zip: Compressing text classification models},
  author={Joulin, Armand and Grave, Edouard and Bojanowski, Piotr and Douze, Matthijs and J{\'e}gou, H{\'e}rve and Mikolov, Tomas},
  journal={arXiv preprint arXiv:1612.03651},
  year={2016}
}
```