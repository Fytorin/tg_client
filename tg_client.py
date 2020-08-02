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
#          -> Подписать                                                 Введите аддрес группы!
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
#
#          -> Имитировать онлайн
#
#          --------------------------------------------------------------------------------------------------
#
#          -> Добавить глазки
#
#          -> Отписаться
#
#
# ограничение функционала:
# 1. почти нигде не обрабатываются неправильно введенные данные
# 2. одновременно можно работать только с одной группой, если начать накручивать подписчиков во вторую,
#    в первой накрутка остановится
# issue 1:   при вводе номера файл .session создаётся сразу же, нужно его удалять, если не
#            подтвердится пароль
# comment 1:   при переходе на главную, нужно очищать всех обработчиков
# comment 2: возможно куча багов и вызыв тем самым баны за счёт отсутствия обработки исключений
# вариант оптимизации: все проценты, разбитые на 20секундные промежутки, можно перенести в отдельный файл

from config import bot_token, api_id, api_hash
from meeting import PrimaryMeeting
from telethon import TelegramClient

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


def main():
    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

    pm = PrimaryMeeting(bot)
    pm.start()

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
