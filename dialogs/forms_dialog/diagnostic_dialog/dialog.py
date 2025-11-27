from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url, Cancel, Back, Next
from aiogram_dialog.widgets.kbd.request import RequestContact
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.media import DynamicMedia


from dialogs.forms_dialog.diagnostic_dialog import getters

from states.state_groups import startSG, DiagnosticSG


diagnostic_dialog = Dialog(
    Window(
        Const('1. Чем занимается ваш бизнес?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_niche_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.niche_choose
            ),
            Next(Const('✍️Другое'), id='get_niche_switcher'),
            width=1
        ),
        Cancel(Const('⬅️Назад'), id='close_dialog'),
        getter=getters.choose_niche_getter,
        state=DiagnosticSG.choose_niche
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_niche',
            on_success=getters.get_niche
        ),
        Back(Const('⬅️Назад'), id='back_choose_niche'),
        state=DiagnosticSG.get_niche
    ),
    Window(
        Const('2. Что отнимает у вас больше всего времени и сил в текущих процессах?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_pain_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.pain_choose
            ),
            Next(Const('✍️Другое'), id='get_pain_switcher'),
            width=1
        ),
        SwitchTo(Const('⬅️Назад'), id='back_choose_niche', state=DiagnosticSG.choose_niche),
        getter=getters.choose_pain_getter,
        state=DiagnosticSG.choose_pain
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_pain',
            on_success=getters.get_pain
        ),
        Back(Const('⬅️Назад'), id='back_choose_pain'),
        state=DiagnosticSG.get_pain
    ),
    Window(
        Const('3. Сколько часов в неделю вы лично тратите на решение этих операционных задач?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_problem_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.problem_choose
            ),
            Next(Const('✍️Другое'), id='get_problem_switcher'),
            width=1
        ),
        SwitchTo(Const('⬅️Назад'), id='back_choose_pain', state=DiagnosticSG.choose_pain),
        getter=getters.choose_problem_getter,
        state=DiagnosticSG.choose_problem
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_problem',
            on_success=getters.get_problem
        ),
        Back(Const('⬅️Назад'), id='back_choose_problem'),
        state=DiagnosticSG.get_problem
    ),
    Window(
        Const('4. Какие инструменты вы уже используете для управления?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_digitalization_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.digitalization_choose
            ),
            Next(Const('✍️Другое'), id='get_digitalization_switcher'),
            width=1
        ),
        SwitchTo(Const('⬅️Назад'), id='back_choose_problem', state=DiagnosticSG.choose_problem),
        getter=getters.choose_digitalization_getter,
        state=DiagnosticSG.choose_digitalization
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_digitalization',
            on_success=getters.get_digitalization
        ),
        Back(Const('⬅️Назад'), id='back_choose_digitalization'),
        state=DiagnosticSG.get_digitalization
    ),
    Window(
        Const('5. Как операционные сложности влияют на ваши финансы?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_finance_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.finance_choose
            ),
            Next(Const('✍️Другое'), id='get_finance_switcher'),
            width=1
        ),
        SwitchTo(Const('⬅️Назад'), id='back_choose_digitalization', state=DiagnosticSG.choose_digitalization),
        getter=getters.choose_finance_getter,
        state=DiagnosticSG.choose_finance
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_finance',
            on_success=getters.get_finance
        ),
        Back(Const('⬅️Назад'), id='back_choose_finance'),
        state=DiagnosticSG.get_finance
    ),
    Window(
        Const('6. Что для вас будет главным результатом успешной автоматизации?'),
        Group(
            Select(
                Format('{item[0]}'),
                id='choose_purpose_builder',
                item_id_getter=lambda x: x[1],
                items='items',
                on_click=getters.purpose_choose
            ),
            Next(Const('✍️Другое'), id='get_purpose_switcher'),
            width=1
        ),
        SwitchTo(Const('⬅️Назад'), id='back_choose_finance', state=DiagnosticSG.choose_finance),
        getter=getters.choose_purpose_getter,
        state=DiagnosticSG.choose_purpose
    ),
    Window(
        Const('📝Введите свой вариант ответа:'),
        TextInput(
            id='get_purpose',
            on_success=getters.get_purpose
        ),
        Back(Const('⬅️Назад'), id='back_choose_purpose'),
        state=DiagnosticSG.get_purpose
    ),
    Window(
        Format('{text}'),
        Column(
            SwitchTo(Const('🧩Запись на глубокий аудит'), id='get_contact_switcher', state=DiagnosticSG.get_contact),
        ),
        getter=getters.audit_result_getter,
        state=DiagnosticSG.audit_result
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
        state=DiagnosticSG.get_contact
    ),
)
