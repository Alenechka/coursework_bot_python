import gensim.downloader as api
import utils

model = api.load("word2vec-ruscorpora-300")
print(model['владик_NOUN'])

topics = ["погода", "настроение", "приветствие"]

test_word = ["привет", ]
top_topic = ["", 0.0]

for topic in topics:
    sim = model.similarity(utils.add_tag_to_word(test_word), utils.add_tag_to_word(topic))

    print(topic + ": " + str(sim))

    if sim > top_topic[1]:
        top_topic = [topic, sim]

print(top_topic)