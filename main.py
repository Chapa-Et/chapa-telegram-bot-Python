from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import LabeledPrice
import logging
import os
import random

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


PROVIDER_TOKEN = os.getenv('CHAPA_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')




def start(update, context):
    """Send a message when the command /start is issued."""
    # get the command argument
    
    update.message.reply_text('Welcome to Chapa Test Shopping Bot! \n This shop is for demo purpose only for @chapapayment_bot')
    try:
        # add button to message and send to channel
        message = update.message
        text = message.text
        chat = message.chat
        if 'start' in text.lower():
            chat_id = chat.id
            title = 'Kirar for Sale!'
            description = 'In Ethiopia and Eritrea played 5-string lyre (krar, kirar). Ready-to-play instrument. Oil finish. It has a beautiful tone und keeps in tune.'
            currency = 'ETB'
            price = 1000 #check telegram doc for decimal point.
            prices = [LabeledPrice("Buy Goods", price * 10)]
            need_shipping_address = False

            context.bot.send_invoice(
                chat_id,
                title,
                description,
                random.randint(10000, 9000000),
                PROVIDER_TOKEN,
                currency,
                prices,
                need_shipping_address=need_shipping_address,
                is_flexible=need_shipping_address,
                photo_url='https://i.etsystatic.com/19083762/r/il/feb451/3712093551/il_fullxfull.3712093551_58y2.jpg',
            )

    except Exception as e:
        import traceback
        traceback.print_exc()
    


def event(update, context):
    print('Message', update)


def main():
    TOKEN = BOT_TOKEN
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    #

    dispatcher.add_handler(MessageHandler(Filters.all, event))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
