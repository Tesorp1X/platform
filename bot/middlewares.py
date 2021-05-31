from datetime import datetime as dt

from aiogram import Dispatcher, types
from aiogram.dispatcher.handler import SkipHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

# from bot.utils import make_broadcast
# from bot.config import bot

STATE_EXPIRE_TIME_IN_SEC = 24 * 3600
ADMINS_IDS = [401961508, 187289003, 400693865, 307306471, 441311056]


class StateValidationMiddleware(BaseMiddleware):
    def __init__(self):
        super(StateValidationMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
            Check if state is expired, if so middleware removes
            the state and skips the current handler.
        """
        dp = Dispatcher.get_current()
        state = dp.current_state()
        data = await state.get_data()

        if 'time' in data:
            # print('time is here!')
            time_delta = (dt.now() - data['time']).total_seconds()
            if time_delta >= STATE_EXPIRE_TIME_IN_SEC:
                await state.reset_state()
                # TODO: create massage for that.
                await message.answer("Вы отвечали слишко долго. Предыдущая операция отмена. Вызываю команду /start.")
                # print('State were removed.')
                raise SkipHandler()

        n = dt.now()
        await state.update_data(_time=n)
        # print("For user {} time set to {}.".format(message.from_user.username, n))
        # print(await state.get_state())


class MessageSourceValidationMiddleware(BaseMiddleware):
    def __init__(self):
        super(MessageSourceValidationMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        Check if message from group chat, if so middleware ignores this message
        """
        if message.chat.id < 0 and message.content_type != 'group_chat_created':
            raise SkipHandler()


class ValidateUserIDMiddleware(BaseMiddleware):
    def __init__(self):
        super(ValidateUserIDMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        Check if message from group chat, if so middleware ignores this message
        """
        from aiogram import Bot
        import os
        bot = Bot(token=os.getenv("API_TOKEN"))

        if message.from_user.id not in ADMINS_IDS:
            message = f'Сообщение от пользователя не из списка админов: {message.from_user.id}\n' \
                      f'First name: {message.from_user.first_name}\n' \
                      f'Last name: {message.from_user.last_name}\n' \
                      f'Username: {message.from_user.username}\n' \
                      f'Text: {message.text}'

            for user in ADMINS_IDS:
                try:
                    await bot.send_message(chat_id=user, text=message, parse_mode=types.ParseMode.MARKDOWN)
                except Exception:
                    print(f"Can't send message chat_id = {user}")

