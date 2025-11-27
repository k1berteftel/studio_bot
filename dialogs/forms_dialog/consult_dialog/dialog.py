from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel, Back, Next
from aiogram_dialog.widgets.kbd.request import RequestContact
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia


from dialogs.forms_dialog.consult_dialog import getters

from states.state_groups import startSG, ConsultSG


consult_dialog = Dialog(
    Window(
        Const('1. Какую задачу вы хотите решить с помощью автоматизации?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_focus_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.focus_choose
            ),
            Next(Const('✍️Другое'), id='get_focus_switcher'),
            width=1
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        getter=getters.choose_focus_getter,
        state=ConsultSG.choose_focus
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_focus',
            on_success=getters.get_focus
        ),
        Back(Const('⬅️Назад'), id='back_choose_focus'),
        state=ConsultSG.get_focus
    ),
    Window(
        Const('2. Как этот процесс организован сейчас?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_process_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.process_choose
            ),
            Next(Const('✍️Другое'), id='get_process_switcher'),
            width=1
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        getter=getters.choose_process_getter,
        state=ConsultSG.choose_process
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_process',
            on_success=getters.get_process
        ),
        Back(Const('⬅️Назад'), id='back_choose_process'),
        state=ConsultSG.get_process
    ),
    Window(
        Const('3. Какие у вас ожидания по срокам и бюджету на решение?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_deadline_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.deadline_choose
            ),
            Next(Const('✍️Другое'), id='get_deadline_switcher'),
            width=1
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        getter=getters.choose_deadline_getter,
        state=ConsultSG.choose_deadline
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_deadline',
            on_success=getters.get_deadline
        ),
        Back(Const('⬅️Назад'), id='back_choose_deadline'),
        state=ConsultSG.get_deadline
    ),
    Window(
        Const('4. Есть ли в команде технический специалист для реализации?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_features_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.features_choose
            ),
            Next(Const('✍️Другое'), id='get_features_switcher'),
            width=1
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        getter=getters.choose_features_getter,
        state=ConsultSG.choose_features
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_features',
            on_success=getters.get_features
        ),
        Back(Const('⬅️Назад'), id='back_choose_features'),
        state=ConsultSG.get_features
    ),
    Window(
        Const('5. Что для вас будет главным показателем успешности консультации?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_criteria_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.criteria_choose
            ),
            Next(Const('✍️Другое'), id='get_criteria_switcher'),
            width=1
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        getter=getters.choose_criteria_getter,
        state=ConsultSG.choose_criteria
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_criteria',
            on_success=getters.get_criteria
        ),
        Back(Const('⬅️Назад'), id='back_choose_criteria'),
        state=ConsultSG.get_criteria
    ),
    Window(
        Const('📞Чтобы мы могли связаться с вами пожалуйста оставьте свои контактные данные'),
        Column(
            RequestContact(Const('📲Поделиться контактом'))
        ),
        MessageInput(
            func=getters.get_contact,
            content_types=ContentType.CONTACT
        ),
        markup_factory=ReplyKeyboardFactory(resize_keyboard=True, one_time_keyboard=True),
        state=ConsultSG.get_contact
    ),
)