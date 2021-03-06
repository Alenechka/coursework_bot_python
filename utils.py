import logging
import re

import config

from pymystem3 import Mystem


# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def add_tag_boosted(text, model, mapping=None):
    processed = model.analyze(text)
    tagged = []
    for w in processed:
        try:
            lemma = w["analysis"][0]["lex"].lower().strip()
            pos = w["analysis"][0]["gr"].split(',')[0]
            pos = pos.split('=')[0].strip()
            if mapping:
                if pos in mapping:
                    pos = mapping[pos]  # здесь мы конвертируем тэги
                else:
                    pos = 'X'  # на случай, если попадется тэг, которого нет в маппинге
            tagged.append(lemma.lower() + '_' + pos)
        except KeyError:
            continue  # я здесь пропускаю знаки препинания, но вы можете поступить по-другому

    return tagged


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


def remove_outofmodel_words(model, message, tag_model, mapping):
    result = list()

    for tagged_word in add_tag_boosted(message, tag_model, mapping):
        if tagged_word in model:
            result.append(tagged_word)

    return result
