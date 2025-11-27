from dialogs.user_dialog.dialog import user_dialog
from dialogs.admin_dialog.dialog import admin_dialog
from dialogs.forms_dialog import consult_dialog, diagnostic_dialog


def get_dialogs():
    return [user_dialog, diagnostic_dialog, consult_dialog, admin_dialog]