from aiogram.fsm.state import State, StatesGroup

# Обычная группа состояний


class startSG(StatesGroup):
    start = State()

    article = State()

    diagnostic = State()

    choose_package = State()
    process_package = State()
    consult_package = State()

    about = State()


class DiagnosticSG(StatesGroup):
    choose_niche = State()
    get_niche = State()

    choose_pain = State()
    get_pain = State()

    choose_problem = State()
    get_problem = State()

    choose_digitalization = State()
    get_digitalization = State()

    choose_finance = State()
    get_finance = State()

    choose_purpose = State()
    get_purpose = State()

    audit_result = State()

    get_contact = State()


class ConsultSG(StatesGroup):
    choose_focus = State()
    get_focus = State()

    choose_process = State()
    get_process = State()

    choose_deadline = State()
    get_deadline = State()

    choose_features = State()
    get_features = State()

    choose_criteria = State()
    get_criteria = State()

    get_contact = State()


class adminSG(StatesGroup):
    start = State()

    get_mail = State()
    get_time = State()
    get_keyboard = State()
    confirm_mail = State()

    deeplink_menu = State()
    deeplink_del = State()

    admin_menu = State()
    admin_del = State()
    admin_add = State()

    form_menu = State()
    get_form_id = State()
    show_form_menu = State()
