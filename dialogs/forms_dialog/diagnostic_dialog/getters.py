from aiogram import Bot
from aiogram.types import CallbackQuery, User, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput, MessageInput

from utils.ai_funcs import get_prompt_answer
from utils.wrapper_funcs import generate_wrapper
from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, DiagnosticSG
from data import diagnostic_answers


config: Config = load_config()


async def choose_niche_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in diagnostic_answers.get('niche').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def niche_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['niche'] = diagnostic_answers['niche'].get(item_id)
    await dialog_manager.switch_to(DiagnosticSG.choose_pain)


async def get_niche(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['niche'] = text
    await dialog_manager.switch_to(DiagnosticSG.choose_pain)


async def choose_pain_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in diagnostic_answers.get('pain').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def pain_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['pain'] = diagnostic_answers['pain'].get(item_id)
    await dialog_manager.switch_to(DiagnosticSG.choose_problem)


async def get_pain(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['pain'] = text
    await dialog_manager.switch_to(DiagnosticSG.choose_problem)


async def choose_problem_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in diagnostic_answers.get('problem').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def problem_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['problem'] = diagnostic_answers['problem'].get(item_id)
    await dialog_manager.switch_to(DiagnosticSG.choose_digitalization)


async def get_problem(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['problem'] = text
    await dialog_manager.switch_to(DiagnosticSG.choose_digitalization)


async def choose_digitalization_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in diagnostic_answers.get('digitalization').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def digitalization_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['digitalization'] = diagnostic_answers['digitalization'].get(item_id)
    await dialog_manager.switch_to(DiagnosticSG.choose_finance)


async def get_digitalization(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['digitalization'] = text
    await dialog_manager.switch_to(DiagnosticSG.choose_finance)


async def choose_finance_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in diagnostic_answers.get('finance').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def finance_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['finance'] = diagnostic_answers['finance'].get(item_id)
    await dialog_manager.switch_to(DiagnosticSG.choose_purpose)


async def get_finance(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    dialog_manager.dialog_data['finance'] = text
    await dialog_manager.switch_to(DiagnosticSG.choose_purpose)


async def choose_purpose_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    buttons = []
    for key, value in diagnostic_answers.get('purpose').items():
        buttons.append(
            (value, key)
        )
    return {
        'items': buttons
    }


async def purpose_choose(clb: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    purpose = diagnostic_answers['purpose'].get(item_id)
    niche = dialog_manager.dialog_data.get('niche')
    pain = dialog_manager.dialog_data.get('pain')
    problem = dialog_manager.dialog_data.get('problem')
    digitalization = dialog_manager.dialog_data.get('digitalization')
    finance = dialog_manager.dialog_data.get('finance')
    await session.add_diagnostic_form(
        user_id=clb.from_user.id,
        niche=niche,
        pain=pain,
        problem=problem,
        digitalization=digitalization,
        finance=finance,
        purpose=purpose
    )
    await clb.message.answer('🙏Спасибо за прохождение опроса')
    diagnostic = dialog_manager.start_data.get('diagnostic')
    if diagnostic:
        await dialog_manager.switch_to(DiagnosticSG.audit_result, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        await dialog_manager.switch_to(DiagnosticSG.get_contact, show_mode=ShowMode.DELETE_AND_SEND)


async def get_purpose(msg: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    purpose = text
    niche = dialog_manager.dialog_data.get('niche')
    pain = dialog_manager.dialog_data.get('pain')
    problem = dialog_manager.dialog_data.get('problem')
    digitalization = dialog_manager.dialog_data.get('digitalization')
    finance = dialog_manager.dialog_data.get('finance')

    await session.add_diagnostic_form(
        user_id=msg.from_user.id,
        niche=niche,
        pain=pain,
        problem=problem,
        digitalization=digitalization,
        finance=finance,
        purpose=purpose
    )
    await msg.answer('🙏Спасибо за прохождение опроса')
    diagnostic = dialog_manager.start_data.get('diagnostic')
    if diagnostic:
        await dialog_manager.switch_to(DiagnosticSG.audit_result, show_mode=ShowMode.DELETE_AND_SEND)
    else:
        await dialog_manager.switch_to(DiagnosticSG.get_contact, show_mode=ShowMode.DELETE_AND_SEND)


async def audit_result_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    bot: Bot = dialog_manager.middleware_data.get('bot')
    form = await session.get_diagnostic_form(event_from_user.id)
    result = await generate_wrapper(
        get_prompt_answer,
        bot,
        event_from_user.id,
        form
    )
    return {
        'text': result
    }


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
    form = await session.get_diagnostic_form(msg.from_user.id)
    for admin_id in config.bot.admin_ids:
        try:
            await msg.bot.send_message(
                chat_id=admin_id,
                text=f'⚙️<b>Новая заявка на <u>бизнес автоматизацию</u></b>\n\nФорма под номером: <code>{form.id}</code>\n'
                     f'Оставленный контакт: <code>{msg.contact.phone_number}</code>\nЮзернейм: '
                     f'{"@" + msg.from_user.username if msg.from_user.username else "-"}'
            )
        except Exception:
            ...
    text = '✅Вы успешно оставили заявку. Мы свяжемся с вами в ближайшее время для уточнения подробностей'
    await msg.answer(text)
    await dialog_manager.start(startSG.start)
