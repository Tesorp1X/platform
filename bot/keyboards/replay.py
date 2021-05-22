from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from bot.constants import DEPARTMENT_OPTIONS, DEGREE_LEVEL_OPTIONS
from bot.db.services.queston_service import *
import typing
from bot.db.services import account_service


def get_department_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for dep in DEPARTMENT_OPTIONS:
        keyboard.add(dep[1])

    return keyboard


def get_degree_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    for dep in DEGREE_LEVEL_OPTIONS:
        keyboard.add(dep[1])

    return keyboard


def get_question_type_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    keyboard.add("Вопрос")
    keyboard.add("Обсуждение")
    keyboard.add("/exit")

    return keyboard


def get_exit_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add("/exit")

    return keyboard


def get_add_finish_exit_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    keyboard.add('/add')
    keyboard.add('/finish')
    keyboard.add('/exit')

    return keyboard


def get_yes_no_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    keyboard.add('Да')
    keyboard.add('Нет')
    keyboard.add('/exit')

    return keyboard


def get_science_list_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    science_list = get_all_sciences()

    for science in science_list:
        keyboard.add(science)

    keyboard.add('/exit')

    return keyboard


def get_subject_list_km(science: str, exclude_list: typing.Optional[dict] = None):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    subject_list = get_all_subjects(science_name=science)

    if exclude_list is not None:
        subject_list = list(set(subject_list) - set(exclude_list.keys()))

    for subject in subject_list:
        keyboard.add(subject)

    keyboard.add('/exit')

    return keyboard


def get_settings_option_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('Name')
    keyboard.add('Department')
    keyboard.add('Degree')
    keyboard.add('Add interest')
    keyboard.add('Delete interest')
    keyboard.add('/exit')

    return keyboard


def get_interests_km(user_id: int):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    interests = account_service.get_all_interests_for_user(user_id)
    for science in interests:
        if isinstance(interests[science], list):
            for subject in interests[science]:
                keyboard.add(science + '/' + subject)
        else:
            keyboard.add(science + '/' + interests[science])

    return keyboard


def get_generic_km(buttons: list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*buttons)

    return keyboard
