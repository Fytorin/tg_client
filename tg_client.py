from config import bot_token, api_id, api_hash
from telethon import TelegramClient, events
from telethon import Button, build_reply_markup
# from telethon import add_event_handler
import asyncio

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


class ConversationBot:

    def __init__(self, _api_id, _api_hash, _bot_token):
        self.bot = TelegramClient('bot', _api_id, _api_hash).start(bot_token=_bot_token)

    def add_event(self, func, event):
        self.bot.add_event_handler(func, event)

    def remove_event(self, func):
        self.bot.remove_event_handler(func)

    def run(self):
        self.bot.run_until_disconnected()

    def stop(self):
        self.bot.disconnect()


# def data_collector_new_client(conversation_bot):

class BotEvents:

    @staticmethod
    async def start_conversation_func(message, bot):
        start_keyboard = [Button.text('Добавить аккаунт'), Button.text('Работать с текущими')]
        markup = bot.build_reply_markup(buttons=start_keyboard)
        await message.respond('Hi!', buttons=markup)
        raise events.StopPropagation

    @staticmethod
    def start_conversation_event():
        return events.NewMessage(pattern='/start')

# @bot.on(events.NewMessage(pattern='Зарегистрировать новый аккаунт'))
# async def add_client(event):
#     await event.respond('Пожалуйста, введите номер телефона')
#
#     async def on_update(event):
#         print(event.text)
#         bot.remove_event_handler (on_update, events.NewMessage)
#         bot.add_event_handler (echo, events.NewMessage)
#
#         #raise events.StopPropagation
#
#
#     bot.add_event_handler(on_update, events.NewMessage)
#     bot.remove_event_handler(echo)
#
#     await event.respond('thanks')
#     raise events.StopPropagation
#     # asyncio.sleep(12)
#
#
# async def echo(event):
#     """Echo the user message."""
#     await event.respond(event.text)


def main():
    """Start the ConversationBot."""
    cb = ConversationBot(api_id, api_hash, bot_token)
    cb.add_event(BotEvents.start_conversation_func,
                 BotEvents.start_conversation_event())
    cb.run()


if __name__ == '__main__':
    main()
