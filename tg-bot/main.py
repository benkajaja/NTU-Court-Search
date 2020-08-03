import configparser
import logging

from telegram import Update, Bot
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

import courtCrawler

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))

crawler = courtCrawler.crawler()

@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


def reply_handler(update: Update, context: CallbackContext):
    """Reply message."""
    text = update.message.text
    # print(text)
    logger.info('Input Text: %s', text)
    # update.message.reply_text(text)
    update.message.reply_text(crawler.getText(text))



# New a dispatcher for bot
dispatcher = Dispatcher(bot, None, use_context=True)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(host = '0.0.0.0',
            port = 5000,
            ssl_context = (config['TELEGRAM']['CERT'], config['TELEGRAM']['KEY']),
            debug = True)
