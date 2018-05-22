import argparse
import logging

from gensim.models import KeyedVectors
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import config

model = None

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


def all_text(bot, update):
    msg = str(update.message.text)
    words = msg.split(" ")

    model.wv.most_similar(positive=[words], negative=["кожура"])


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
    dp.add_handler(MessageHandler(Filters.text, all_text))

    updater.start_polling()

    logging.info("Polling started.")


def init_model():
    """Init Word2Vec model."""

    global model
    model = KeyedVectors.load_word2vec_format("C:\\Users\\Vladislav\\Downloads\\ruscorpora_upos_skipgram_300_5_2018.vec"
                                              "\\ruscorpora_upos_skipgram_300_5_2018.vec")

    logging.info("Model is loaded.")


if __name__ == "__main__":
    # Prepare arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("token", help="Bot token", type=str)
    args = parser.parse_args()

    # Run bot
    run_bot(args.token)
    # init_model()
