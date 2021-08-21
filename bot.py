"""Telegram bot/app/interface for VkusVill courier API."""

import logging
from threading import Event
from typing import Union, Callable

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from api import VkusVillCourierAPI
from util import BOT_TOKEN, COURIER_ID, VKUSVILL_TOKEN

api = VkusVillCourierAPI(COURIER_ID, VKUSVILL_TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

START_MESSAGE = """
Hi, I'm a VkusVill courier bot! I can help you manage and automate your parcel delivery. Type /parcels to see all parcels.
"""

prepare_set = set()
ready_set = set()
taken_set = set()


def start(update, context):
    """Start command handler callback function."""
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=START_MESSAGE)


def parcels(update: Update, context: CallbackContext):
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


def check(update: Update, context: CallbackContext):
    """Check for updated parcel state periodically and notify."""
    global prepare_set, ready_set, taken_set
    try:
        # Possible HTTPError, ValueError
        prepare = api.get_parcels_prepare()
        ready = api.get_parcels_ready()
        taken = api.get_parcels_taken()

        for p in prepare:
            if p.id not in prepare_set:
                context.bot.send_message(
                    update.effective_chat.id,
                    f"New parcel!\n{p.distance}m, {p.weight}kg"
                )
                context.bot.send_location(
                    update.effective_chat.id,
                    p.latitude,
                    p.longitude
                )
                prepare_set.add(p.id)

        for p in ready:
            if p.id not in ready_set:
                context.bot.send_message(
                    update.effective_chat.id,
                    f"Parcel is ready!\n{p.distance}m, {p.weight}kg"
                )
                ready_set.add(p.id)

    except Exception as e:
        raise Exception() from e


def periodic(period: Union[int, float], func: Callable):
    """Periodically run passed function."""
    ticker = Event()
    while not ticker.wait(period):
        func()


def main():
    """Start bot."""
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    parcels_handler = CommandHandler('parcels', parcels)
    echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
    check_handler = CommandHandler(
        'check', lambda u, c: periodic(3, lambda: check(u, c)))

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(parcels_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(check_handler)

    updater.start_polling()


if __name__ == "__main__":
    main()
