from aiogram import types
from aiogram.dispatcher import FSMContext

from bot import constants
from bot.config import dp
from bot.states import RegistrationProcessStates, NewQuestionStates, AdminPanelStates
import bot.keyboards.replay as kb
from bot.db.services import account_service, queston_service
from bot.handlers.commands import send_welcome, handle_admin

'''
    Getting current state 'name':
        cs = await state.get_state()
        print(cs.split(':')[1])
'''

'''
# Attempt to make a generic handler...

@dp.message_handler(state=RegistrationProcessStates.all_states)
async def registration_process(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    current_state = current_state.strip(':')[1]
    user_data = await state.get_data()
    user_data[current_state] = message.text
    if current_state == 'degree_level':
        telegram_data = message.from_user
        account_service.add_new_user(t_id=telegram_data.id,
                                     t_username=telegram_data.username,
                                     name=user_data['name'],
                                     email=user_data['email'],
                                     department=user_data['department'],
                                     degree_level=user_data['degree_level'],
                                     )
        await message.answer("Регистрация прошла успешно! Добро пожаловать!", reply_markup=kb.ReplyKeyboardRemove())
        await state.finish()
        await send_welcome(message)

    else:
'''


@dp.message_handler(user_id=401961508, state=AdminPanelStates.waiting_for_section)
async def handle_admin_add_section(message: types.Message, state: FSMContext):
    section = message.text
    await state.update_data(section=section)

    await message.answer("Выберите науку для нового раздела \"{}\".".format(section),
                         reply_markup=kb.get_science_list_km())
    # cycle through science and subject selection.
    await state.set_state(AdminPanelStates.waiting_for_science)


@dp.message_handler(user_id=401961508, state=AdminPanelStates.waiting_for_subject)
async def handle_admin_add_subject(message: types.Message, state: FSMContext):
    subject = message.text
    data = await state.get_data()
    section = data.get('section')
    if section is not None:
        science = data.get('science')
        # save section in db
        try:
            queston_service.add_new_section(name=section, subject_name=subject)
            await message.answer(
                "Раздел \"{}\" добавлен в предмет \"{}\"/\"{}\".".format(section, science, subject),
                reply_markup=kb.ReplyKeyboardRemove())
        except queston_service.DoesNotExist:
            await message.answer("Ошибка! Что-то пошло не так...", reply_markup=kb.ReplyKeyboardRemove())

        await state.reset_data()
        await state.set_state(AdminPanelStates.waiting_for_command)
        await handle_admin(message, state)
    else:
        # go to science selection and save subject here
        await state.update_data(subject=subject)
        await message.answer("Выберите науку из списка.", reply_markup=kb.get_science_list_km())
        await state.set_state(AdminPanelStates.waiting_for_science)


@dp.message_handler(user_id=401961508, state=AdminPanelStates.waiting_for_science)
async def handle_admin_add_science(message: types.Message, state: FSMContext):
    science = message.text
    data = await state.get_data()

    subject = data.get('subject')
    section = data.get('section')
    if subject is not None:
        # checking if its from handle_admin_add_subject
        # save subject in db
        try:
            queston_service.add_new_subject(name=subject, science_name=science)
            await message.answer(
                "Наука {} выбрана для предмета \"{}\". Возвращение к админ-панели".format(science, subject),
                reply_markup=kb.ReplyKeyboardRemove())
        except queston_service.DoesNotExist:
            await message.answer("Ошибка! Что-то пошло не так...", reply_markup=kb.ReplyKeyboardRemove())

        await state.reset_data()
        await state.set_state(AdminPanelStates.waiting_for_command)
        await handle_admin(message, state)
    elif section is not None:
        # checking if its from handle_admin_add_section
        # go to subject selection and save in subject handler
        await state.update_data(science=science)
        await message.answer("Выберите предмет из списка.", reply_markup=kb.get_subject_list_km(science=science))
        await state.set_state(AdminPanelStates.waiting_for_subject)

    else:
        # save science in db
        queston_service.add_new_science(name=science)
        await message.answer("Наука \"{}\" добавлена.".format(science), reply_markup=kb.ReplyKeyboardRemove())
        await state.reset_data()
        await state.set_state(AdminPanelStates.waiting_for_command)
        await handle_admin(message, state)


@dp.message_handler(state=RegistrationProcessStates.waiting_for_degree_level)
async def registration_complete(message: types.Message, state: FSMContext):
    telegram_data = message.from_user
    user_data = await state.get_data()
    user_data['degree_level'] = message.text
    # TODO: FIX how department and degree_level are being saved.
    account_service.add_new_user(t_id=telegram_data.id,
                                 t_username=telegram_data.username,
                                 name=user_data['name'],
                                 email=user_data['email'],
                                 department=user_data['department'],
                                 degree_level=user_data['degree_level'],
                                 )
    await message.answer("Регистрация прошла успешно! Добро пожаловать!", reply_markup=kb.ReplyKeyboardRemove())
    await state.finish()
    await send_welcome(message)


@dp.message_handler(state=RegistrationProcessStates.waiting_for_department)
async def registration_department(message: types.Message, state: FSMContext):
    await state.update_data(department=message.text)
    await message.answer("На каком ты уровне обучения?" + constants.REGISTRATION_EXIT_SENTENCES,
                         reply_markup=kb.get_degree_km())
    await RegistrationProcessStates.next()


@dp.message_handler(state=RegistrationProcessStates.waiting_for_email)
async def registration_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)

    await message.answer("С какого ты факультета?" + constants.REGISTRATION_EXIT_SENTENCES,
                         reply_markup=kb.get_department_km())
    await RegistrationProcessStates.next()


@dp.message_handler(state=RegistrationProcessStates.waiting_for_name)
async def registration_name(message: types.Message, state: FSMContext):
    await state.set_data({'name': message.text, })
    await message.answer("Твой адрес эл. почты (только для лохов из НГУ)." + constants.REGISTRATION_EXIT_SENTENCES,
                         reply_markup=kb.ReplyKeyboardRemove())
    await RegistrationProcessStates.next()


# /new process

@dp.message_handler(state=NewQuestionStates.waiting_for_type)
async def new_question_type(message: types.Message, state: FSMContext):
    if message.text not in ['Вопрос', 'Обсуждение']:
        await message.answer('Выбери корректный тип, используя клавиатуру.', reply_markup=kb.get_question_type_km())
        return

    answer = ''
    if message.text == 'Вопрос':
        await state.set_data({'type': 'question'})
        answer = 'Введи название вопроса. Постарайся быть максмально конкретным.'
    elif message.text == 'Обсуждение':
        await state.set_data({'type': 'discussion'})
        answer = 'Введи название обсуждения. Постарайся быть максмально конкретным.'

    await message.answer(answer)
    await NewQuestionStates.next()


@dp.message_handler(state=NewQuestionStates.waiting_for_title)
async def new_question_title(message: types.Message, state: FSMContext):
    pass


@dp.message_handler(state="*")
async def handle_any_other_message(message: types.Message, state: FSMContext):
    await message.answer("Ошибка! Невозможно выполнить эту команду сейчас!")
    await send_welcome(message)
