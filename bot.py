"""Telegram bot/app/interface for VkusVill courier API."""

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from api import VkusVillCourierAPI
from util import BOT_TOKEN, COURIER_ID, VKUSVILL_TOKEN

api = VkusVillCourierAPI(COURIER_ID, VKUSVILL_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

START_MESSAGE = """Hi, I'm a VkusVill courier bot! I can help you manage and automate your parcel delivery. Type /parcels to see all parcels.
"""


def start(update, context):
    """Start command handler callback function."""
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=START_MESSAGE)


def parcels(update, context):
    """Return prepare, ready and taken parcels."""
    try:
        # Possible HTTPError, ValueError
        prepare = api.get_parcels_prepare()
        ready = api.get_parcels_ready()
        taken = api.get_parcels_taken()

        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Prepare: {prepare}")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Ready: {ready}")
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Taken: {taken}")
    except Exception as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"API error: {e}")


def echo(update, context):
    """Echos all sent messages."""
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


def main():
    """Start bot."""
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    parcels_handler = CommandHandler('parcels', parcels)
    echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(parcels_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


if __name__ == "__main__":
    main()
