from .langid import LID

_CACHE = {}

def detect(text, **params):
    if 'model' not in _CACHE:
        _CACHE['model'] = LID()
    return _CACHE['model'].predict(text, **params)
