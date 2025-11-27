from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import SwitchTo, Column, Row, Button, Group, Select, Start, Url
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.media import DynamicMedia

from dialogs.user_dialog import getters

from states.state_groups import startSG, adminSG, DiagnosticSG, ConsultSG

user_dialog = Dialog(
    Window(
        DynamicMedia('media'),
        Format('Здравствуйте, {name} 🤚, это чат-бот <b>Leggit Tech</b>\n\nЯ помогу вам найти точки роста и '
               'избавиться от операционных проблем в вашем бизнесе.\nВыберите, с чего начнем:'),
        Column(
            SwitchTo(Const('🎁Для бизнеса'), id='article_switcher', state=startSG.article),
            SwitchTo(Const('💡Бесплатная диагностика'), id='diagnostic_switcher', state=startSG.diagnostic),
            SwitchTo(Const('🤝Оставить заявку'), id='choose_package_switcher', state=startSG.choose_package),
            Url(Const('📲Связаться с нами'), id='contact_url', url=Const('https://t.me/Leggit_dev')),
            SwitchTo(Const('ℹ️Работа с нами'), id='about_switcher', state=startSG.about),
            Start(Const('Админ панель'), id='admin', state=adminSG.start, when='admin')
        ),
        getter=getters.start_getter,
        state=startSG.start
    ),
    Window(
        Const('⌛️Как освободить <b>20 часов в неделю</b> от операционных задач\nЧитайте ниже'),
        Column(
            Url(Const('📖Читать'), id='article_url',
                url=Const('https://telegra.ph/Kak-osvobodit-20-chasov-v-nedelyu-ot-operacionnyh-zadach-11-24')),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.article
    ),
    Window(
        Const('🤖Чтобы наш ИИ-ассистент смог провести <b>качественную диагностику</b> ваших '
              'бизнес-процессов, пожалуйста пройдите опрос'),
        Column(
            Button(Const('📋Пройти опрос'), id='start_diagnostic_form', on_click=getters.diagnostic_switcher),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.diagnostic
    ),
    Window(
        DynamicMedia('media'),
        Format('{text}'),
        Column(
            Url(Const('📲Связаться с нами'), id='contact_url', url=Const('https://t.me/Leggit_dev')),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        getter=getters.about_getter,
        state=startSG.about
    ),
    Window(
        Const('🧑‍💻Мы оказываем <b>2 пакета услуг</b>:\n • Автоматизация бизнес-процессов под ключ ⚙️ + 🚀\n • '
              'Консультация для бизнеса по автоматизации 🗣️ + 📊\nВыберите интересующую вас услугу👇'),
        Column(
            SwitchTo(Const('Автоматизировать бизнес-процессы'), id='process_package_switcher', state=startSG.process_package),
            SwitchTo(Const('Записаться на консультацию'), id='consult_package_switcher', state=startSG.consult_package),
        ),
        SwitchTo(Const('⬅️Назад'), id='back', state=startSG.start),
        state=startSG.choose_package
    ),
    Window(
        Const('Пожалуйста пройдите короткий опрос из 6 вопросов, чтобы мы могли мы получили необходимые вводные данные '
              'для дальнейшей работы с вами'),
        Column(
            Start(Const('📋Пройти опрос'), id='start_diagnostic_form', state=DiagnosticSG.choose_niche),
        ),
        SwitchTo(Const('⬅️Назад'), id='back_choose_package', state=startSG.choose_package),
        state=startSG.process_package
    ),
    Window(
        Const('Пожалуйста ответьте на 5 коротких вопросов, чтобы наша консультация была максимально продуктивной.'
              '\nЭто поможет нам понять вашу задачу и подготовить конкретные варианты решений'),
        Column(
            Start(Const('📋Пройти опрос'), id='start_consult_form', state=ConsultSG.choose_focus),
        ),
        SwitchTo(Const('⬅️Назад'), id='back_choose_package', state=startSG.choose_package),
        state=startSG.consult_package
    )
)