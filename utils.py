import logging
import re

import config

from pymystem3 import Mystem


# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def add_tag_to_word(word):
    m = Mystem()
    processed = m.analyze(word)[0]
    lemma = processed["analysis"][0]["lex"].lower().strip()
    pos = processed["analysis"][0]["gr"].split(',')[0]
    pos = pos.split('=')[0].strip()
    tagged = lemma + '_' + transform_tag(pos)

    return tagged


def transform_tag(tag):
    if tag == "S":
        return "NOUN"
    elif tag == "COM" or tag == "A" or tag == "ANUM":
        return "ADJ"
    elif tag == "ADV" or tag == "ADVPRO":
        return "ADV"
    elif tag == "APRO":
        return "DET"
    elif tag == "CONJ":
        return "SCONJ"
    elif tag == "INTJ":
        return "INTJ"
    elif tag == "NONLEX":
        return "X"
    elif tag == "NUM":
        return "NUM"
    elif tag == "PART":
        return "PART"
    elif tag == "PR":
        return "ADP"
    elif tag == "SPRO":
        return "PRON"
    elif tag == "UNKN":
        return "X"
    elif tag == "V":
        return "VERB"
    else:
        return tag


def remove_tag(tagged_word):
    return str(tagged_word).split("_")[0]


def load_topics():
    result = list()

    with open(config.TOPICS_FILE, 'r', encoding='utf-8') as file:
        for line in file.readlines():
            result.append(line.replace("\n", ""))

        return result


def remove_excess_symbols(message):
    regex = re.compile('[^a-zA-Zа-яА-я\s]')
    return regex.sub('', message).replace('\n', ' ').strip()


def remove_outofmodel_words(model, message):
    result = list()

    for word in message:
        tagged_word = add_tag_to_word(word)
        if tagged_word in model:
            result.append(tagged_word)

    return result
