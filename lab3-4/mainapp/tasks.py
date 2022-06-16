from celery import shared_task
from lab3.settings import BOT_TOKEN, KEY_TELEGRAM
import telebot
from time import sleep

bot = telebot.TeleBot(BOT_TOKEN)


@shared_task
def make_order(*args):
    sleep(5)
    message = "New order!\n"

    for arg in args:
        if arg is not None:
            message += arg + "\n"

    bot.send_message(KEY_TELEGRAM, message)


