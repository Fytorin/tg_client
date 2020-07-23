#               COMMANDS                                                    TEXT
# # /start                                                              Добро пожаловать в главное меню!
#
#          -> Добавить юзера                                            Пожалуйста, введите номер телефона
#
#            -> Enter                                                   Пожалуйста, введите полученный код
#
#              -> Enter                                                 Ваш аккаунт был добавлен/не добавлен
#
#                -> Главное меню                                        Добро пожаловать в главное меню!
#
#          -> Подписаться                                               Введите аддрес группы!
#
#            -> Ввёл аддрес!                                            Введите число подписчиков
#
#              -> Ввёл число!                                           Введите время, около которого будут
#                                                                       происходить подписки
#
#                -> Ввёл время!                                         Введите размер одного стандартного
#                                                                       отклонения(подписка будет около
#                                                                       стандартного распределения) в минутах
#
#                  -> Ввёл размер!                                      Заввка сформирована
#
#                    -> Главное меню                                    Добро пожаловать в главное меню!


#          -> Добавить глазки
#
#          -> Отписаться
#
#          -> Имитировать онлайн
#
# issue 1:   при переходе на главную, нужно очищать всех обработчиков
# issue 2:   при вводе номера файл .session создаётся сразу же, нужно его удалять, если не
#            подтвердится пароль


from config import bot_token, api_id, api_hash
from telethon import TelegramClient, events
from telethon import Button
# from telethon import add_event_handler
import asyncio

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


class MainHandler:
    def __init__(self, bot):
        self.bot = bot

    async def start_processing(self, message):
        start_keyboard = [[Button.text('Добавить юзера'), Button.text('xПодписаться')],
                          [Button.text('xДобавить глазки'), Button.text('xОтписаться')],
                          [Button.text('xИмитировать онлайн')]]
        markup = self.bot.build_reply_markup(buttons=start_keyboard)
        markup.single_use = True
        await message.respond('Добро пожаловать в главное меню!', buttons=markup)
        raise events.StopPropagation

    def add_response_to_start(self):
        event = events.NewMessage(pattern='/start|На главную')
        self.bot.add_event_handler(self.start_processing, event)
        # self.bot.remove_event_handler

    async def new_user_processing(self, message):
        new_user_no_phone_keyboard = [Button.text('На главную')]
        markup = self.bot.build_reply_markup(buttons=new_user_no_phone_keyboard)
        markup.resize = True
        await message.respond('Пожалуйста, введите номер телефона', buttons=markup)
        add_new_user(self.bot)
        raise events.StopPropagation

    def add_response_to_new_user_request(self):
        event = events.NewMessage(pattern='Добавить юзера')
        self.bot.add_event_handler(self.new_user_processing, event)

    def add_all_responses_from_start_menu_from_start_menu(self):
        self.add_response_to_new_user_request()
        self.add_response_to_start()


def add_new_user(bot):
    user_creator = NewUserCreator(bot)
    user_creator.add_response_to_phone_off()
    user_creator.add_response_to_code_off()


class NewUserCreator:
    def __init__(self, bot):
        self.phone = None
        self.code = None
        self.bot = bot
        self.tg_id_parent = None
        self.name_new_child = None
        self.phone_code_hash = None

    def registration_user(self):
        pass

    def add_response_to_phone_off(self):
        event = events.NewMessage()
        self.bot.add_event_handler(self.phone_off_processing, event)

    async def phone_off_processing(self, message):
        print('phone off processing')
        self.phone = message.text
        self.tg_id_parent = message.sender_id
        self.name_new_child = await self.get_name_for_new_client()
        new_client = TelegramClient(self.name_new_child, api_id, api_hash)
        await new_client.connect()
        await new_client.sign_in(self.phone)
        sent_code = await new_client.send_code_request(self.phone)
        self.phone_code_hash = sent_code.phone_code_hash
        await message.respond('Пожалуйста, введите код')
        self.bot.remove_event_handler(self.phone_off_processing)
        raise events.StopPropagation

    async def get_name_for_new_client(self):
        import os
        all_files = os.listdir()
        num_exists_children = 0
        for file_name in all_files:
            if file_name.find(str(self.tg_id_parent)) != -1 and file_name.find('.session') != -1:
                num_exists_children += 1
        return str(self.tg_id_parent) + '_' + str(num_exists_children)
    
    def add_response_to_code_off(self):
        event = events.NewMessage()
        self.bot.add_event_handler(self.code_off_processing, event)

    async def code_off_processing(self, message):
        print('code off processing')
        self.code = message.text
        print(self.code, self.phone)
        client = TelegramClient(self.name_new_child, api_id, api_hash)
        await client.connect()
        await client.sign_in(phone=self.phone, code=self.code, phone_code_hash=self.phone_code_hash)
        self.bot.remove_event_handler(self.code_off_processing)
        raise events.StopPropagation
    

def main():
    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    main_hd = MainHandler(bot)
    main_hd.add_all_responses_from_start_menu_from_start_menu()

    bot.run_until_disconnected()


if __name__ == '__main__':
    main()


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
