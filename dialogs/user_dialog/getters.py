from aiogram.types import CallbackQuery, User, Message, ContentType
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.input import ManagedTextInput

from database.action_data_class import DataInteraction
from config_data.config import load_config, Config
from states.state_groups import startSG, DiagnosticSG


config: Config = load_config()


async def start_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    session: DataInteraction = dialog_manager.middleware_data.get('session')
    admin = False
    admins = [*config.bot.admin_ids]
    admins.extend([admin.user_id for admin in await session.get_admins()])
    if event_from_user.id in admins:
        admin = True
    media = MediaAttachment(type=ContentType.PHOTO, path='medias/Навигация.png')
    return {
        'media': media,
        'name': event_from_user.full_name,
        'admin': admin
    }


async def diagnostic_switcher(clb: CallbackQuery, widget: Button, dialog_manager: DialogManager):
    data = {
        'diagnostic': True
    }
    await dialog_manager.start(DiagnosticSG.choose_niche, data=data)


async def about_getter(event_from_user: User, dialog_manager: DialogManager, **kwargs):
    text = ('<b>Пакеты услуг:</b>\n\n<b>1)🗣️ + 📊Консультация по автоматизации:</b>\n<em>Точечный разбор вашей задачи с '
            'готовым планом действий и рекомендациями инструментов.</em>\n\n<b>2)⚙️ + 🚀Автоматизация под ключ:</b>\n'
            '<em>Полный цикл: от глубокого аудита до внедрения, тестирования и поддержки работающей системы.</em>\n\n'
            '<b>Этапы работы (для пакета «Под ключ»):</b>\n1. Диагностика → Анализ болей и первичная оценка\n'
            '2. Глубокий аудит → Детальный разбор процессов (AS-IS)\n3. Проектирование → Создание решения и ТЗ (TO-BE)'
            '\n4. Договор → Фиксируем стоимость, сроки и KPI\n5. Реализация → Внедрение, тестирование, обучение\n'
            '6. Поддержка → Гарантийное обслуживание\n\n<b>Ваши гарантии:</b>\n• <u>Фиксированная цена</u> и сроки '
            'по ТЗ\n• <u>Поэтапная оплата</u> по факту выполнения\n• <u>Прозрачность</u>: еженедельные отчеты и '
            'трекер\n• <u>Результат</u>: KPI в договоре и передача исходных кодов\n• <u>Конфиденциальность</u> (NDA) '
            'и <u>1 месяц</u> гарантии')
    media = MediaAttachment(type=ContentType.PHOTO, path='medias/Услуги.png')
    return {
        'media': media,
        'text': text
    }