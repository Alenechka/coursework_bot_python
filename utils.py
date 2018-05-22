from pymystem3 import Mystem


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
    elif tag == "COM":
        return "ADJ"
    else:
        return tag


def remove_tag(tagged_word):
    return str(tagged_word).split("_")[0]