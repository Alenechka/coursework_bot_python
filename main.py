import argparse
import logging
import gensim
import gensim.downloader
import config

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import utils

model = None
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

    msg = str(update.message.text)
    words_from_message = utils.remove_outofmodel_words(model, utils.remove_excess_symbols(msg).split(" "))
    logging.info("Words in model from message: %s." % words_from_message)
    logging.info("Try to identify topic ...")
    topic_for_message = ["", 0.0]

    for topic in topics:
        score = model.n_similarity(words_from_message, [utils.add_tag_to_word(topic)])

        logging.info("Score for topic '{0}' is {1}.".format(topic, str(score)))

        if score > topic_for_message[1]:
            topic_for_message = [topic, score]

    logging.info("Identified topic is '%s'. " % topic_for_message[0])

    update.message.reply_text("Тема: '%s'." % topic_for_message[0], quote=True)


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

    updater.start_polling()

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


if __name__ == "__main__":
    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="Bot token", type=str)
    args = parser.parse_args()

    # Run bot
    init_model()
    run_bot(args.token)
