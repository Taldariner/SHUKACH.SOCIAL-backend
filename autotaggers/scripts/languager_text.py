import py3langid as langid


def identify_lang(text):
    lang, prob = langid.classify(text)
    return lang
