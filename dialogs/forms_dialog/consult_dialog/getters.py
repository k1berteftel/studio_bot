from aiogram import Bot
from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, ConsultSG
from data import consult_answers


config: Config = load_config()


async def choose_focus_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in consult_answers.get('focus').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def focus_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['focus'] = consult_answers['focus'].get(item_id)
    await dialog_manager.switch_to(ConsultSG.choose_process)


async def get_focus(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['focus'] = text
    await dialog_manager.switch_to(ConsultSG.choose_process)


async def choose_process_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in consult_answers.get('process').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def process_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['process'] = consult_answers['process'].get(item_id)
    await dialog_manager.switch_to(ConsultSG.choose_deadline)


async def get_process(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['process'] = text
    await dialog_manager.switch_to(ConsultSG.choose_deadline)


async def choose_deadline_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in consult_answers.get('deadline').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def deadline_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['deadline'] = consult_answers['deadline'].get(item_id)
    await dialog_manager.switch_to(ConsultSG.choose_features)


async def get_deadline(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['deadline'] = text
    await dialog_manager.switch_to(ConsultSG.choose_features)


async def choose_features_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in consult_answers.get('features').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def features_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['features'] = consult_answers['features'].get(item_id)
    await dialog_manager.switch_to(ConsultSG.choose_criteria)


async def get_features(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['features'] = text
    await dialog_manager.switch_to(ConsultSG.choose_criteria)


async def choose_criteria_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in consult_answers.get('criteria').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def criteria_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    criteria = consult_answers['criteria'].get(item_id)
    focus = dialog_manager.dialog_data.get('focus')
    process = dialog_manager.dialog_data.get('process')
    deadline = dialog_manager.dialog_data.get('deadline')
    features = dialog_manager.dialog_data.get('features')
    await session.add_consult_form(
        user_id=clb.from_user.id,
        focus=focus,
        process=process,
        deadline=deadline,
        features=features,
        criteria=criteria
    )
    await clb.message.answer('🙏Спасибо за прохождение опроса')
    await dialog_manager.switch_to(ConsultSG.get_contact, show_mode=ShowMode.DELETE_AND_SEND)


async def get_criteria(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    criteria = text
    focus = dialog_manager.dialog_data.get('focus')
    process = dialog_manager.dialog_data.get('process')
    deadline = dialog_manager.dialog_data.get('deadline')
    features = dialog_manager.dialog_data.get('features')
    await session.add_consult_form(
        user_id=msg.from_user.id,
        focus=focus,
        process=process,
        deadline=deadline,
        features=features,
        criteria=criteria
    )
    await msg.answer('🙏Спасибо за прохождение опроса')
    await dialog_manager.switch_to(ConsultSG.get_contact, show_mode=ShowMode.DELETE_AND_SEND)


async def get_contact(msg: Message, widget: MessageInput, dialog_manager: DialogManager):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    if dialog_manager.has_context():
        await dialog_manager.done()
        try:
            await msg.bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id - 1)
        except Exception:
            ...
        counter = 1
        while dialog_manager.has_context():
            await dialog_manager.done()
            try:
                await msg.bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id + counter)
            except Exception:
                ...
            counter += 1
    form = await session.get_consult_form(msg.from_user.id)
    for admin_id in config.bot.admin_ids:
        try:
            await msg.bot.send_message(
                chat_id=admin_id,
                text=f'⚙️<b>Новая заявка на <u>консультацию</u></b>\n\nФорма под номером: <code>{form.id}</code>\n'
                     f'Оставленный контакт: <code>{msg.contact.phone_number}</code>\nЮзернейм: '
                     f'{"@" + msg.from_user.username if msg.from_user.username else "-"}'
            )
        except Exception:
            ...
    text = '✅Вы успешно оставили заявку. Мы свяжемся с вами в ближайшее время для уточнения подробностей'
    await msg.answer(text)
    await dialog_manager.start(startSG.start)
