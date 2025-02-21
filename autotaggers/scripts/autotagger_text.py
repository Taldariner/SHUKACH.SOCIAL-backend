import re

import spacy
from keyword_spacy import KeywordExtractor


AUTOTAGGERS_VERSION = 2
SUPPORTED_LANGUAGES = {
    "uk" : "uk_core_news_lg",
    "en" : "en_core_web_lg",
    "ru" : "ru_core_news_lg",
}


def clean_entities(doc, nlp):
    entities            = []
    normalized_entities = []

    for ent in doc.ents:
        cleaned_text = re.sub(r'[\r\n]+', ' ', ent.text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        lemmatized_tokens = [token.lemma_.capitalize() if token.is_title
                             else token.lemma_.upper() if token.is_upper
                             else token.lemma_ for token in nlp(cleaned_text)]
        lemmatized_text = " ".join(lemmatized_tokens)
        entities.append((lemmatized_text, ent.label_))

    entities = sorted(set(entities), key = lambda x: x[1])

    for entity in entities:
        if not any(entity[0] in other[0] and entity[0] != other[0] for other in entities):
            normalized_entities.append(entity)

    for i, entity in enumerate(normalized_entities):
        if entity[1] == "GPE":
            normalized_entities[i] = (entity[0], "LOC")

    normalized_entities = [entity for entity in normalized_entities if entity[1] not in ["NORP", "FAC", "EVENT", "WORK_OF_ART",
                                                                                         "LAW", "LANGUAGE", "DATE", "TIME",
                                                                                         "PERCENT", "MONEY", "QUANTITY", "ORDINAL", "CARDINAL"]]
    return sorted(normalized_entities, key = lambda x: (x[1], x[0]))


def clean_keywords(doc, nlp):
    keywords_nouns = []
    keywords_sorted = sorted(doc._.keywords, key = lambda x: x[2], reverse = True)

    for keyword, sentence, score in keywords_sorted:
        
        cleaned_keyword = re.sub(r'[\r\n]+', ' ', keyword)
        cleaned_keyword = re.sub(r'\s+',     ' ', cleaned_keyword)
        
        if cleaned_keyword:
            token = nlp(cleaned_keyword)[0]
            if token.pos_ == "NOUN":
                keywords_nouns.append((token.lemma_, score))

    return keywords_nouns


def clean_hashtags(text):
    hashtags = re.findall(r'#\w+', text)
    
    cleaned_hashtags = [re.sub(r'[\r\n]+', ' ', tag) for tag in hashtags]
    cleaned_hashtags = [re.sub(r'\s+',     ' ', tag) for tag in cleaned_hashtags]

    hashtags_snake_case = ['#' + re.sub(r'([a-zа-я])([A-ZА-Я])|_+', r'\1_\2', tag[1:]).lower().replace('__', '_') for tag in cleaned_hashtags]
    hashtags_sorted = sorted(hashtags_snake_case)
    
    return hashtags_sorted


def pipeline_texts(texts, model_name):
    nlp = spacy.load(model_name)
    nlp.add_pipe("keyword_extractor", last = True, config = {"top_n": 20, "min_ngram": 1, "max_ngram": 1, "strict": False, "top_n_sent": 3})
    
    docs = [nlp(text) for text in texts]

    norm_entities = [clean_entities(doc, nlp) for doc in docs]
    norm_keywords = [clean_keywords(doc, nlp) for doc in docs]
    norm_hashtags = [clean_hashtags(text) for text in texts]

    return norm_entities, norm_keywords, norm_hashtags
