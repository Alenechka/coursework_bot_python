import argparse
import logging
import gensim
import gensim.downloader
import requests
from future import standard_library
from pymystem3 import Mystem

import config

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import utils

model = None
tags_model = None
tag_mapping = None
topics = []

# Enable logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text("I'm Alina's bot for word2vec bullshit.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def identify_topic(bot, update):
    logging.info("Identify message topic ...")

    if "505903005" == str(update.message.from_user.id).strip() or \
            "363314646" == str(update.message.from_user.id).strip():
        msg = str(update.message.text)
        words_from_message = utils.remove_outofmodel_words(model, msg,
                                                           tags_model, tag_mapping)

        if words_from_message and len(words_from_message) > 0:
            logging.info("Words in model from message: %s." % words_from_message)
            logging.info("Try to identify topic ...")
            topic_for_message = ["", 0.0]
            topics_scores = {}

            for topic in topics:
                if topic in model:
                    score = model.n_similarity(words_from_message, [topic])

                    logging.info("Score for topic '{0}' is {1}.".format(topic, str(score)))

                    topics_scores[topic] = score

                    if score > topic_for_message[1]:
                        topic_for_message = [utils.remove_tag(topic), score]

            logging.info("Identified topic is '%s'. " % topic_for_message[0])

            # update.message.reply_text("Рассчет косинусной меры для всех тем: '%s'." % topics_scores, quote=True)
            update.message.reply_text("Тема сообщения: '%s'." % topic_for_message[0], quote=True)
        else:
            update.message.reply_text("Не удалось определить тему сообщения.", quote=True)


def run_bot(token):
    """Start the bot."""

    logging.info("Start bot with token: '%s'." % args.token)

    updater = Updater(token,
                      request_kwargs={'proxy_url': config.PROXY_URL,
                                      'urllib3_proxy_kwargs': {'username': config.PROXY_USER,
                                                               'password': config.PROXY_PASS}}
                      )

    dp = updater.dispatcher
    dp.add_error_handler(error)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, identify_topic))

    updater.start_polling(clean=True)

    logging.info("Polling started.")


def init_model():
    """Init Word2Vec model."""

    logging.info("Loading model '%s' ..." % config.MODEL_NAME)

    global model
    model = gensim.downloader.load(config.MODEL_NAME)
    logging.info("Model is loaded.")

    global topics
    topics = utils.load_topics()
    logging.info("Topics: %s." % topics)

    global tags_model
    standard_library.install_aliases()

    # Таблица преобразования частеречных тэгов Mystem в тэги UPoS:
    mapping_url = 'https://raw.githubusercontent.com/akutuzov/universal-pos-tags/4653e8a9154e93fe2f417c7fdb7a357b7d6ce333/ru-rnc.map'

    global tag_mapping
    mystem2upos = {}
    r = requests.get(mapping_url, stream=True)
    for pair in r.text.split('\n'):
        pair = pair.split()
        if len(pair) > 1:
            mystem2upos[pair[0]] = pair[1]

    tag_mapping = mystem2upos

    logging.info('Loading the tags model ...')
    tags_model = Mystem()


if __name__ == "__main__":
    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="Bot token", type=str)
    args = parser.parse_args()

    # Run bot
    init_model()
    run_bot(args.token)
