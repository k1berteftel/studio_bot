from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager, StartMode

from database.action_data_class import DataInteraction
from states.state_groups import startSG


user_router = Router()


@user_router.message(CommandStart())
async def start_dialog(msg: Message, dialog_manager: DialogManager, session: DataInteraction, command: CommandObject, state: FSMContext):
    args = command.args
    #referral = None
    link = None
    if args not in ['article', 'diagnostic']:
        link_ids = await session.get_links()
        ids = [i.link for i in link_ids]
        if args in ids:
            await session.add_admin(msg.from_user.id, msg.from_user.full_name)
            await session.del_link(args)
        if not await session.check_user(msg.from_user.id):
            deeplinks = await session.get_deeplinks()
            deep_list = [i.link for i in deeplinks]
            if args in deep_list:
                link = args
                await session.add_entry(args)
            #try:
                #args = int(args)
                #users = [user.user_id for user in await session.get_users()]
                #if args in users:
                    #referral = args
                    #await session.add_refs(args)
            #except Exception as err:
                #print(err)
    await session.add_user(msg.from_user.id, msg.from_user.username if msg.from_user.username else 'Отсутствует',
                           msg.from_user.full_name, link)
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
    member = await msg.bot.get_chat_member(
        chat_id=-1002577435324,
        user_id=msg.from_user.id
    )
    if member.status == 'left':
        await state.update_data(switcher=args)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='🔗Подписаться', url='https://t.me/+fzFaVHkNHJ4yNTQy')],
                [InlineKeyboardButton(text='✅Проверить', callback_data='check_sub')]
            ]
        )
        await msg.answer('🙏Чтобы продолжить пользоваться ботом пожалуйста подпишитесь на канал', reply_markup=keyboard)
        return
    if args:
        if args == 'diagnostic':
            await dialog_manager.start(state=startSG.diagnostic, mode=StartMode.RESET_STACK)
        elif args == 'article':
            await dialog_manager.start(state=startSG.article, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)


@user_router.callback_query(F.data == 'check_sub')
async def check_sub(clb: CallbackQuery, dialog_manager: DialogManager, state: FSMContext):
    member = await clb.bot.get_chat_member(
        chat_id=-1002577435324,
        user_id=clb.from_user.id
    )
    if member.status == 'left':
        await clb.answer('❗️Вы все еще не подписались на канал')
        return
    data = await state.get_data()
    switcher = data.get('switcher')
    if switcher:
        if switcher == 'diagnostic':
            await dialog_manager.start(state=startSG.diagnostic, mode=StartMode.RESET_STACK)
        elif switcher == 'article':
            await dialog_manager.start(state=startSG.article, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(state=startSG.start, mode=StartMode.RESET_STACK)
    await state.clear()
