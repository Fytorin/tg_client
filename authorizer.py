from telethon import TelegramClient, events, Button
from config import api_id, api_hash


class UserAuthorizer:

    def __init__(self, bot):
        self.phone = None
        self.code = None
        self.bot = bot
        self.tg_id_parent = None
        self.name_new_child = None
        self.phone_code_hash = None

    def start(self):
        self.add_response_to_new_user_request()

    def add_response_to_new_user_request(self):
        event = events.NewMessage(pattern='Добавить юзера')
        self.bot.add_event_handler(self.new_user_processing, event)

    async def new_user_processing(self, message):
        new_user_no_phone_keyboard = [Button.text('На главную')]
        markup = self.bot.build_reply_markup(buttons=new_user_no_phone_keyboard)
        markup.resize = True
        await message.respond('Пожалуйста, введите номер телефона', buttons=markup)
        self.bot.remove_event_handler(self.new_user_processing)
        self.add_response_to_mining_phone()
        self.add_response_to_mining_code()
        raise events.StopPropagation

    def add_response_to_mining_phone(self):
        event = events.NewMessage()
        self.bot.add_event_handler(self.mining_phone_processing, event)

    async def mining_phone_processing(self, message):
        self.phone = message.text
        self.tg_id_parent = message.sender_id
        self.name_new_child = await self.get_name_for_new_client()
        new_client = TelegramClient(self.name_new_child, api_id, api_hash)
        await new_client.connect()
        await new_client.sign_in(self.phone)
        sent_code = await new_client.send_code_request(self.phone)
        self.phone_code_hash = sent_code.phone_code_hash
        await message.respond('Пожалуйста, введите код')
        await new_client.disconnect()
        self.bot.remove_event_handler(self.mining_phone_processing)
        raise events.StopPropagation

    async def get_name_for_new_client(self):
        import os
        all_files = os.listdir()
        num_exists_children = 0
        for file_name in all_files:
            if file_name.find(str(self.tg_id_parent)) != -1 and file_name.find('.session') != -1:
                num_exists_children += 1
        return str(self.tg_id_parent) + '_' + str(num_exists_children)

    def add_response_to_mining_code(self):
        event = events.NewMessage()
        self.bot.add_event_handler(self.mining_code_processing, event)

    async def mining_code_processing(self, message):
        self.code = message.text
        print(self.code, self.phone)
        client = TelegramClient(self.name_new_child, api_id, api_hash)
        await client.connect()
        markup = self.bot.build_reply_markup(buttons=[Button.text('На главную')])
        try:
            print('try register')
            await client.sign_in(phone=self.phone, code=self.code, phone_code_hash=self.phone_code_hash)
            await message.respond('Поздравляем, регистрация прошла успешно')
        except:
            print('except register')
            import os
            os.remove(self.name_new_child + '.session')
            await message.respond('Код введён неверно!', buttons=markup)
        self.bot.remove_event_handler(self.mining_code_processing)
        raise events.StopPropagation
