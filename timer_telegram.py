import ptbot
import os
from pytimeparse import parse


def notify(time_is_over):
    bot.send_message(telegram_id_chat, time_is_over)


def notify_progress(secs_left, update_message, full_time):
    bot.update_message(telegram_id_chat, update_message,
                       'Left {} {}'.format(secs_left, ' seconds') + '\n' + render_progressbar(full_time, secs_left))


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def reply(msg_time):
    user_time = str(parse('{}'.format(msg_time)))
    message_id = bot.send_message(telegram_id_chat, 'Timer started on {} {}'.format(user_time, 'seconds.'))
    bot.create_timer(parse('{}'.format(msg_time)), notify, "Time is over.")
    bot.create_countdown(parse('{}'.format(msg_time)), notify_progress, update_message=message_id,
                         full_time=int(user_time))


telegram_id_chat = os.getenv("TELEGRAM_ID_CHAT")
telegram_id_token = os.getenv("TELEGRAM_ID_TOKEN")
bot = ptbot.Bot(telegram_id_token)
bot.send_message(telegram_id_chat, "How long to start the timer?")
bot.wait_for_msg(reply)
