from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import JoinChannelRequest
from config import api_id, api_hash


def percentage_of_subscriptions_at_a_time(time):
    # до 300 секунд:
    def early_function(x):
        return -0.00054444476684489124 * (x ** 2) + 0.30878497326644360754 * x

    # с 300 до 3600 секунд:
    def middle_function(x):
        return -0.00000000040397860512 * (x ** 3) - 0.00000002394383454962 * (x ** 2) + 0.01477805052588987422 * x

    # с 3600 до 90000 секунд:
    def ending_function(x):
        return -0.00000000000008982989 * (x ** 3) + 0.00000000823989147498 * (x ** 2) + 0.00017513223999156280 * x

    if time <= 300:
        return early_function(time)
    elif time <= 3600:
        return early_function(300) + middle_function(time)
    elif time <= 90000:
        return early_function(300) + middle_function(3600) + ending_function(time)
    else:
        return early_function(300) + middle_function(3600) + ending_function(90000)


# def check_work_percentage_function():
#     print('time: 0', percentage_of_subscriptions_at_a_time(0))
#     print('time: 1', percentage_of_subscriptions_at_a_time(1))
#     print('time: 10', percentage_of_subscriptions_at_a_time(10))
#     print('time: 60', percentage_of_subscriptions_at_a_time(60))
#     print('time: 240', percentage_of_subscriptions_at_a_time(240))
#     print('time: 300', percentage_of_subscriptions_at_a_time(300))
#     print('time: 360', percentage_of_subscriptions_at_a_time(360))
#     print('time: 3480', percentage_of_subscriptions_at_a_time(3480))
#     print('time: 3600', percentage_of_subscriptions_at_a_time(3600))
#     print('time: 3720', percentage_of_subscriptions_at_a_time(3720))
#     print('time: 70000', percentage_of_subscriptions_at_a_time(70000))


class UserSigner:

    def __init__(self, bot):
        self.bot = bot
        self.num_of_required_subscribers = None
        self.link_on_group = None
        self.tg_id_parent = None

    def start(self):
        self.add_response_to_sign_users_request()

    def add_response_to_sign_users_request(self):
        event = events.NewMessage(pattern='Подписать')
        self.bot.add_event_handler(self.sign_users_processing, event)

    async def sign_users_processing(self, message):
        sign_users_keyboard = [Button.text('На главную')]
        markup = self.bot.build_reply_markup(buttons=sign_users_keyboard)
        markup.resize = True
        await message.respond('Пожалуйста, введите число подписчиков!', buttons=markup)
        self.add_response_to_mining_num_of_required_subscribers()
        self.add_response_to_mining_link_of_target_group()
        raise events.StopPropagation

    def add_response_to_mining_num_of_required_subscribers(self):
        event = events.NewMessage()
        self.bot.add_event_handler(self.mining_num_of_required_subscribers_processing, event)

    async def mining_num_of_required_subscribers_processing(self, message):
        print('mining num of required users')
        self.num_of_required_subscribers = message.text
        await message.respond('Пожалуйста, введите куда подписаться!')
        self.bot.remove_event_handler(self.mining_num_of_required_subscribers_processing)
        raise events.StopPropagation

    def add_response_to_mining_link_of_target_group(self):
        event = events.NewMessage()
        self.bot.add_event_handler(self.mining_link_of_target_group_processing, event)

    async def mining_link_of_target_group_processing(self, message):
        print('mining link')
        sign_users_keyboard = [Button.text ('На главную')]
        markup = self.bot.build_reply_markup (buttons=sign_users_keyboard)
        markup.resize = True
        self.link_on_group = message.text
        self.tg_id_parent = message.sender_id
        self.bot.remove_event_handler(self.mining_link_of_target_group_processing)
        await message.respond('Процесс запущен!', buttons=markup)
        await self.start_cheating()
        raise events.StopPropagation

    async def start_cheating(self):
        # Подписываюсь следующим образом: каждые 20 секунд отправляю запрос на процент людей,
        #                                 которые должны подписаться к указанному моменту времени,
        #                                 разницу в процентах между текущим запросом и предыдущим перевожу
        #                                 в число людей, добавляю его к предыдущему полученному числу и
        #                                 запускаю цикл, который каждую секунду отнимает по 1 от полученного
        #                                 числа и добавляет одного человека в группу до тех пор, пока
        #                                 полученное число не станет меньше 1
        import time
        list_clients = self.get_list_exists_clients()
        current_time = 20
        delta_time = 20
        num_of_subscribers = 0
        num_of_people_signed = 0
        while current_time <= 90000:
            current_percentage = percentage_of_subscriptions_at_a_time(current_time)
            previous_percentage = percentage_of_subscriptions_at_a_time(current_time - delta_time)
            delta_percentage = current_percentage - previous_percentage
            num_of_subscribers += (delta_percentage / 100) * self.num_of_required_subscribers
            while num_of_subscribers >= 1:
                # subscribe a person to the group
                client_name = list_clients[num_of_people_signed]
                client = TelegramClient(client_name, api_id, api_hash)
                await client.connect()
                await client(JoinChannelRequest(self.link_on_group))
                num_of_subscribers -= 1
                num_of_people_signed += 1
            time.sleep(delta_time)
            current_time += delta_time

    def get_list_exists_clients(self):
        import os
        target_list = []
        all_files = os.listdir()
        for file_name in all_files:
            if file_name.find(str(self.tg_id_parent)) != -1 and file_name.find('.session') != -1:
                target_list.append(file_name)
        return target_list
