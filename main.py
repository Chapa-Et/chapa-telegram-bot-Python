#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""Basic example for a bot that can receive payment from user."""

import logging
from dotenv import load_dotenv
load_dotenv()
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
       
    )
from telegram import LabeledPrice, ShippingOption, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


PROVIDER_TOKEN = os.getenv('CHAPA_TOKEN')
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    msg = (
        "Use /shipping to get an invoice for shipping-payment, or /noshipping for an "
        "invoice without shipping."
    )

    await update.message.reply_text(msg)


async def start_with_shipping_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends an invoice with shipping-payment."""
    chat_id = update.message.chat_id
    title = "Kirar For Sale"
    description = "Kirar For Sale to Test a very simple BOT"
    # select a payload just for you to recognize its the donation from your bot
    payload = "I-LOVE-CHAPA"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    currency = "ETB"
    # price in birr
    price = 100
    # price * 100 so as to include 2 decimal points
    # check https://core.telegram.org/bots/payments#supported-currencies for more details
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    await context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        PROVIDER_TOKEN,
        currency,
        prices,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )


async def start_without_shipping_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Sends an invoice without shipping-payment."""
    chat_id = update.message.chat_id
    title = "Kirar For Sale"
    description = "Kirar For Sale to Test a very simple BOT"
    # select a payload just for you to recognize its the donation from your bot
    payload = "I-LOVE-CHAPA"
    # In order to get a provider_token see https://core.telegram.org/bots/payments#getting-a-token
    currency = "ETB"
    # price in birr
    price = 100
    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Test", price * 100)]

    # optionally pass need_name=True, need_phone_number=True,
    # need_email=True, need_shipping_address=True, is_flexible=True
    await context.bot.send_invoice(
        chat_id, title, description, payload, PROVIDER_TOKEN, currency, prices
    )


async def shipping_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "I-LOVE-CHAPA":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
        return

    # First option has a single LabeledPrice
    options = [ShippingOption("1", "Shipping Option A", [
                              LabeledPrice("A", 100)])]
    # second option has an array of LabeledPrice objects
    price_list = [LabeledPrice("B1", 150), LabeledPrice("B2", 200)]
    options.append(ShippingOption("2", "Shipping Option B", price_list))
    await query.answer(ok=True, shipping_options=options)


# after (optional) shipping, it's the pre-checkout
async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers the PreQecheckoutQuery"""
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != "I-LOVE-CHAPA":
        # answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
    else:
        await query.answer(ok=True)


# finally, after contacting the payment provider...
async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    await update.message.reply_text("Thank you for your payment!")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # simple start function
    application.add_handler(CommandHandler("start", start_callback))

    # Add command handler to start the payment invoice
    application.add_handler(CommandHandler(
        "shipping", start_with_shipping_callback))
    application.add_handler(CommandHandler(
        "noshipping", start_without_shipping_callback))

    # Optional handler if your product requires shipping
    application.add_handler(ShippingQueryHandler(shipping_callback))

    # Pre-checkout handler to final check
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    application.add_handler(
        MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback)
    )

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
