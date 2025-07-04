import nltk
from nltk.corpus import cmudict
import re

def get_difficult_phones():
    return {'TH': ['θ', 'ð'], 'R': ['r'], 'L': ['l'], 'V': ['v'], 'NG': ['ŋ'], 'Z': ['z']}

def analyze_text(text):
    nltk.download('punkt', quiet=True)
    nltk.download('cmudict', quiet=True)
    d = cmudict.dict()
    words = nltk.word_tokenize(text)
    difficult_phones = get_difficult_phones()
    difficult_words = {}
    knowledge_points = {'现在进行时 (-ing)': [], '名词复数 (-s/-es)': []}
    for word in words:
        lw = word.lower()
        if lw in d:
            phones = [p for pron in d[lw] for p in pron]
            for key, phone_list in difficult_phones.items():
                for phone in phone_list:
                    if phone.upper() in [ph.upper() for ph in phones]:
                        if lw not in difficult_words:
                            difficult_words[lw] = []
                        difficult_words[lw].append(f'包含易错音 /{phone}/')
        if re.search(r'ing$', lw):
            knowledge_points['现在进行时 (-ing)'].append(word)
        if re.search(r's$|es$', lw):
            knowledge_points['名词复数 (-s/-es)'].append(word)
    knowledge_points = {k: v for k, v in knowledge_points.items() if v}
    return {'difficult_words': difficult_words, 'knowledge_points': knowledge_points}