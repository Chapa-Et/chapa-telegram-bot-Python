from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ShippingQueryHandler
from telegram import LabeledPrice, ShippingOption
import logging
import os

from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


CHAPA_TOKEN = os.getenv('CHAPA_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')

PROVIDER_TOKEN = CHAPA_TOKEN



def start(update, context):
    """Send a message when the command /start is issued."""
    # get the command argument
    
    update.message.reply_text('Well come to Chapa Test Shopping Bot! \n This shop is for demo purpose only for @chapapayment_bot')
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
            price = 100
            prices = [LabeledPrice("Test", price * 100)]
            need_shipping_address = False

            if 'shipping' in text.lower():
                description += ' shipping'
                need_shipping_address = True
            else:
                description += ' no shipping'

            context.bot.send_invoice(
                chat_id,
                title,
                description,
                PROVIDER_TOKEN,
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
    


def channel_post(update, context):
    try:
        # add button to message and send to channel
        message = update.message
        text = message.text
        chat = message.chat
        if 'chapa' in text.lower():
            chat_id = chat.id
            title = 'Kirar for Sale'
            description = 'In Ethiopia and Eritrea played 5-string lyre (krar, kirar). Ready-to-play instrument. Oil finish. It has a beautiful tone und keeps in tune.'
            currency = 'ETB'
            price = 100
            prices = [LabeledPrice("Test", price * 100)]
            need_shipping_address = False

            if 'shipping' in text.lower():
                description += ' shipping'
                need_shipping_address = True
            else:
                description += ' no shipping'
            
            context.bot.send_invoice(
                chat_id,
                title,
                description,
                PROVIDER_TOKEN,
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

def shipping_callback(update, context):
    """Answers the ShippingQuery with ShippingOptions"""

    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != PROVIDER_TOKEN:
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
        return

    # First option has a single LabeledPrice
    options = [ShippingOption('1', 'Shipping Option A', [LabeledPrice('A', 100)])]
    # second option has an array of LabeledPrice objects
    price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
    options.append(ShippingOption('2', 'Shipping Option B', price_list))
    query.answer(ok=True, shipping_options=options)



def main():
    TOKEN = BOT_TOKEN
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    #
    dispatcher.add_handler(MessageHandler(
        Filters.chat_type, channel_post))
    dispatcher.add_handler(ShippingQueryHandler(shipping_callback))
    dispatcher.add_handler(MessageHandler(Filters.all, event))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
