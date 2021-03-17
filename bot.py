from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, CallbackContext
import logging 
from typing import Dict
import re

updater = Updater(token="1442056081:AAEYidrAK0c8Tj9uKdXqFlzLd6H7WATW38M", use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

#States 
Wishlist, CHOOSING, MAKE= range(3)

def start(update: Update, context:CallbackContext) -> int:
    update.message.reply_text("""WELCOME TO HAPPYGIFT ME!!!\n\n To enter an item into your 
                              wishlist, use the command /make.\n\n To see your wishlist, please use the 
                              /wishlist command.\n\n To see another person's wishlist, please use the 
                              /see command""")
    return Wishlist

def make(update: Update, context:CallbackContext) -> int:
    update.message.reply_text("""To enter an item into your wishlist, send a message to the bot in the format
                              'index. item' (eg. '1. Toy'). \nPlease only enter 1 item at a time.""")
    return MAKE

def wishlist(update: Update, context: CallbackContext) -> int:
    wishlist = []
    if context.user_data:
        wishlist.extend(f"{key}. {value[0]}" for (key, value) in context.user_data.items())
    else:
        wishlist.append("The wishlist is empty")
    update.message.reply_text('\n'.join(wishlist))
    return MAKE

def gethandle(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Who\'s wishlist would you like to see?') 
    return CHOOSING

def otherswishlist(update: Update, context: CallbackContext) -> int:
    text = update.message.text 
    if (text[0] != '@'):
        update.message.reply_text('Please enter valid telegram handle starting with @')
    else:
        update.message.reply_text(f'{text}\'s wishlist is:\n 1. Toy\n 2. Board game')
    return CHOOSING

INFO_REGEX = r'(.+)\. (.+)'
def receive_info(update: Update, context: CallbackContext) -> int:
    info = re.match(INFO_REGEX, update.message.text).groups()
    context.user_data[info[0]] = [info[1]]
    update.message.reply_text(f"{info[1]} added to wishlist")
    return MAKE

def done(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END

dispatcher.add_handler(ConversationHandler(
    entry_points = [CommandHandler('start', start)], 
    states={
        Wishlist: [CommandHandler('make', make), CommandHandler('wishlist', wishlist), CommandHandler('see', gethandle)],
        CHOOSING : [MessageHandler(Filters.text & ~(Filters.command), otherswishlist), CommandHandler('see', gethandle)],
        MAKE: [MessageHandler(Filters.regex("(.+). (.+)"), receive_info), CommandHandler('done', done), 
               CommandHandler('wishlist', wishlist), CommandHandler('done', done), CommandHandler('see', gethandle)]            },
    fallbacks = 
    [MessageHandler(Filters.regex('^Done$'), done)])
)
    

updater.start_polling()

updater.idle()
