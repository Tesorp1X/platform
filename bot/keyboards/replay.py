from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from bot.constants import DEPARTMENT_OPTIONS, DEGREE_LEVEL_OPTIONS
from bot.db.services.queston_service import *


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

    return keyboard


def get_science_list_km():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    science_list = get_all_sciences()

    for science in science_list:
        keyboard.add(science)

    return keyboard


def get_subject_list_km(science: str):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    subject_list = get_all_subjects(science_name=science)

    for subject in subject_list:
        keyboard.add(subject)

    return keyboard

