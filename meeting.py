from telethon import TelegramClient, events, Button
from authorizer import UserAuthorizer


class PrimaryMeeting:

    def __init__(self, bot):
        self.bot = bot

    def start(self):
        self.add_response_to_start()

    def add_response_to_start(self):
        event = events.NewMessage(pattern='/start|На главную')
        self.bot.add_event_handler(self.start_processing, event)
        # self.bot.remove_event_handler

    async def start_processing(self, message):
        start_keyboard = [[Button.text('Добавить юзера'), Button.text('xПодписаться')],
                          [Button.text('xДобавить глазки'), Button.text('xОтписаться')],
                          [Button.text('xИмитировать онлайн')]]
        markup = self.bot.build_reply_markup(buttons=start_keyboard)
        markup.single_use = True
        await message.respond('Добро пожаловать в главное меню!', buttons=markup)
        ua = UserAuthorizer(self.bot)
        ua.start()
        raise events.StopPropagation

