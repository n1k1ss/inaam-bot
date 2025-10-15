from aiogram import Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from aiogram.enums import ParseMode
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.types import WebAppInfo, CopyTextButton
from aiogram.exceptions import TelegramBadRequest

from handlers.get_date import get_datetime
from handlers.db import db
from handlers.generate_excel import export_to_excel
from handlers.only_admin import only_admin_access
from handlers.get_current_balance import get_current_balance
from inaam_bot_logger import logger

class Form(StatesGroup):
    adding_price_waiting = State()
    removing_price_waiting = State()
    expense_amount_waiting = State()

def get_adm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📈 💰", callback_data="incr_balance"),
            InlineKeyboardButton(text="📉 💰", callback_data="decr_balance")
        ],
        [
            InlineKeyboardButton(text="Excel 📄 (месяц)", callback_data="download_excel_month"),
            InlineKeyboardButton(text="Excel 📄 (1/4 года)", callback_data="download_excel_quarter")
        ],
        [
            InlineKeyboardButton(text="Excel 📄 (1/2 года)", callback_data="download_excel_half"),
            InlineKeyboardButton(text="Excel 📄 (год)", callback_data="download_excel_year")
        ]
    ])

def get_wor_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Траты 💸", callback_data="expenses"),
            InlineKeyboardButton(text="🔄", callback_data="refresh_balance")
        ]
    ])

def get_website_link_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сайт 🌐", web_app=WebAppInfo(url="https://inaam.ru"))
        ],
        [
            InlineKeyboardButton(text="Почта 📨", copy_text=CopyTextButton(text="info@inaam.ru")),
            InlineKeyboardButton(text="Телефон 📞", copy_text=CopyTextButton(text="+79852320202"))
        ],
        [
            InlineKeyboardButton(text="Telegram 💬", url="t.me/oleynik_INAAM")
        ]
    ])

def get_confirm_adm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да ✅", callback_data="add_balance_yes"),
            InlineKeyboardButton(text="Нет ❌", callback_data="add_balance_no")
        ]
    ])

def get_confirm_expense_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да ✅", callback_data="c_expense"),
            InlineKeyboardButton(text="Нет ❌", callback_data="r_expense")
        ]
    ])

def get_confirm_adding_new_main_adm(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data=f"c_main#{user_id}"),
            InlineKeyboardButton(text="❌", callback_data=f"r_main#{user_id}")
        ]
    ])

def get_confirm_adding_new_wor(user_id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅", callback_data=f"c_work#{user_id}"),
            InlineKeyboardButton(text="❌", callback_data=f"r_work#{user_id}")
        ]
    ])

def get_expenses_type() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Транспорт 🚌", callback_data="exp-transport"),
            InlineKeyboardButton(text="...", callback_data="exp-extra")
        ]
    ])

async def handle_excel_export(call: CallbackQuery, period: str):
    loading = await call.message.answer("<b>Генерация файла...</b> ⏳", parse_mode=ParseMode.HTML)
    output = await export_to_excel(period)
    if output:
        file = BufferedInputFile(output.read(), filename=f"inaam expenses {period}.xlsx")
        await call.message.answer_document(file)
        await loading.edit_text("<b>Готово</b> ✅", parse_mode=ParseMode.HTML)
    else:
        await loading.edit_text("<b>Нет данных</b> 📂", parse_mode=ParseMode.HTML)



def register_adm_callbacks(dp: Dispatcher, bot: Bot):
    @dp.callback_query()
    @only_admin_access(db, "both")
    async def callback(call: CallbackQuery, state: FSMContext):
        if call.data == "incr_balance":
            await call.message.edit_text(
                "<b>На сколько вы хотите увеличить баланс?</b> 💰📈",
                parse_mode=ParseMode.HTML)

            await state.set_state(Form.adding_price_waiting)

        if call.data == "decr_balance":
            await call.message.edit_text(
                "<b>На сколько вы хотите уменьшить баланс?</b> 💰📉",
                parse_mode=ParseMode.HTML)

            await state.set_state(Form.removing_price_waiting)

        if call.data == "add_balance_yes" and (await state.get_data()).get("adding_balance_amount") is not None:
            try:
                price_to_add = (await state.get_data()).get("adding_balance_amount")
                current_balance = await get_current_balance()

                logger.warning(f"[{call.from_user.id}] Произошло изменение баланса [{call.from_user.first_name}] [{price_to_add}₽] [{current_balance}₽ -> {current_balance + price_to_add}₽]")

                await state.clear()

                await db.execute('UPDATE balance SET amount = amount + $1', price_to_add)
                await call.message.edit_text("<b>Добавлено</b> 💰✅\n/start", parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.exception(f"[{call.from_user.id}] Ошибка в callback [add_balance_yes (admin_keyboard.py)] [{e}]")
                await call.message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

        if call.data == "add_balance_no":
            await state.clear()
            await call.message.edit_text(
                "<b>Отменено</b> ❌",
                parse_mode=ParseMode.HTML
            )

        if call.data == "c_expense" and (await state.get_data()).get("expense_amount") is not None and (await state.get_data()).get("expense_type") is not None:
            try:
                day = await get_datetime("day")
                month = await get_datetime("month")
                year = await get_datetime("year")
                amount = (await state.get_data()).get("expense_amount")
                type = (await state.get_data()).get("expense_type")

                logger.warning(f"[{call.from_user.id}] Новая трата [{call.from_user.first_name}] [{type}] [{amount}₽]")

                await db.execute('INSERT INTO balance_expenses (doer, doer_username, section, day, month, year, amount) VALUES ($1, $2, $3, $4, $5, $6, $7)', call.from_user.first_name, call.from_user.username, type, day, month, year, amount)
                await db.execute('UPDATE balance SET amount = amount - $1', amount)
                await call.message.edit_text("<b>Добавлено</b> 💰✅\n/start", parse_mode=ParseMode.HTML)
                await state.clear()
            except Exception as e:
                logger.exception(f"[{call.from_user.id}] Ошибка в callback [c_expense (admin_keyboard.py)] [{e}]")
                await call.message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

        if call.data == "r_expense":
            await state.clear()
            await call.message.edit_text(
                "<b>Отменено</b> ❌",
                parse_mode=ParseMode.HTML
            )

        if call.data.startswith("download_excel_"):
            period = call.data.split("_")[-1]
            logger.warning(f"[{call.from_user.id}] Скачан файл Excel [{period}]")
            await handle_excel_export(call, period)

        if call.data == "expenses":
            await call.message.edit_text("<b>Выберите раздел:</b> 🏷", parse_mode=ParseMode.HTML, reply_markup=get_expenses_type())

        if call.data == "refresh_balance":
            try:
                current_balance = await get_current_balance
                
                await call.message.edit_text(f"<b>Привет, {call.from_user.first_name}</b> 👋\n<b>Роль:</b> <i>Работник</i> 👨‍💻\n💸 <b>Баланс:</b> <i>{current_balance}₽</i>", parse_mode=ParseMode.HTML, reply_markup=call.message.reply_markup)
            except TelegramBadRequest as e:
                if "message is not modified" in e.message.lower():
                    await call.answer("Баланс не изменился 💰", show_alert=True)

            except Exception as e:
                logger.exception(f"[{call.from_user.id}] Ошибка обновления баланса [admin_keyboard.py] [{e}]")
                await call.message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

        if call.data == "exp-transport":
            await call.message.edit_text("<b>Тип:</b> <b>Транспорт</b> 🚌\n<i>Сколько потратили?</i>", parse_mode=ParseMode.HTML)
            await state.update_data(expense_type="Транспорт")
            await state.set_state(Form.expense_amount_waiting)

        if call.data == "exp-extra":
            await call.message.edit_text("<b>Тип:</b> <b>...</b>\n<i>Сколько потратили?</i>", parse_mode=ParseMode.HTML)
            await state.update_data(expense_type="Extra")
            await state.set_state(Form.expense_amount_waiting)

        if call.data.startswith("c_main#"):
            try:
                user_id = int(call.data.split("#")[1])
                person = await db.fetchrow('SELECT 1 FROM main_admin_ids WHERE id=$1', user_id)
                if not person:
                    logger.warning(f"[{call.from_user.id} -> {user_id}] Новая роль [Администратор 👨‍💼]")
                    await db.execute('DELETE FROM worker_ids WHERE id=$1', user_id)
                    await db.execute('INSERT INTO main_admin_ids (id) VALUES ($1) ON CONFLICT DO NOTHING', user_id)
                    await call.message.edit_caption(caption="<b>Добавление завершено</b> ✅", parse_mode=ParseMode.HTML)
                    await bot.send_message(user_id, "<b>Ваша роль была обновлена!</b> 👤\n/start", parse_mode=ParseMode.HTML)
                else:
                    await call.message.edit_caption(caption="<b>Человек и так уже админ</b> ❌", parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.exception(f"[{call.from_user.id}] Ошибка в callback [c_main#... (admin_keyboard.py)] [{e}]")
                await call.message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

        if call.data.startswith("r_main#"):
            user_id = int(call.data.split("#")[1])
            await bot.send_message(user_id, "<b>Заявка отклонена</b> ❌\n<b>Роль:</b> <i>Администратор</i> 👨‍💼", parse_mode=ParseMode.HTML)
            await call.message.edit_caption(caption="<b>Добавление отменено</b> ❌", parse_mode=ParseMode.HTML)

        if call.data.startswith("c_work#"):
            try:
                user_id = int(call.data.split("#")[1])
                person = await db.fetchrow('SELECT 1 FROM worker_ids WHERE id=$1', user_id)
                if not person:
                    logger.warning(f"[{call.from_user.id} -> {user_id}] Новая роль [Работник 👨‍💼]")
                    await db.execute('DELETE FROM main_admin_ids WHERE id=$1', user_id)
                    await db.execute('INSERT INTO worker_ids (id) VALUES ($1) ON CONFLICT DO NOTHING', user_id)
                    await call.message.edit_caption(caption="<b>Добавление завершено</b> ✅", parse_mode=ParseMode.HTML)
                    await bot.send_message(user_id, "<b>Ваша роль была обновлена!</b> 👤\n/start", parse_mode=ParseMode.HTML)
                else:
                    await call.message.edit_caption(caption="<b>Человек и так уже работник</b> ❌", parse_mode=ParseMode.HTML)
            except Exception as e:
                logger.exception(f"[{call.from_user.id}] Ошибка в callback [c_work#... (admin_keyboard.py)] [{e}]")
                await call.message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

        if call.data.startswith("r_work#"):
            user_id = int(call.data.split("#")[1])
            await bot.send_message(user_id, "<b>Заявка отклонена</b> ❌\n<b>Роль:</b> <i>Работник</i> 👨‍💻", parse_mode=ParseMode.HTML)
            await call.message.edit_caption(caption="<b>Добавление отменено</b> ❌", parse_mode=ParseMode.HTML)

        await call.answer()

    @dp.message(Form.adding_price_waiting)
    async def adding_price_process(message: Message, state: FSMContext):
        try:
            price = message.text
            await message.delete()
            if price.isdigit():
                price = int(price)
                await state.update_data(adding_balance_amount=price)

                await message.answer(
                    f"<b>Вы пополняете баланс на {price:,}₽</b> 💰\n<i>Верно?</i>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_confirm_adm_keyboard()
                    )
            else:
                await message.answer(
                    f"<b>Неправильный ввод! Введите целое положительное число!</b> ❌",
                    parse_mode=ParseMode.HTML,
                    )
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в FSM [Form.adding_price_waiting (admin_keyboard.py)] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

    @dp.message(Form.removing_price_waiting)
    async def removing_price_process(message: Message, state: FSMContext):
        try:
            price = message.text
            await message.delete()
            if price[1:].isdigit() and price[0] == "-":
                price = int(price)
                await state.update_data(adding_balance_amount=price)

                await message.answer(
                    f"<b>Вы уменьшаете баланс на {price:,}₽</b> 💰\n<i>Верно?</i>",
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_confirm_adm_keyboard()
                    )
            else:
                await message.answer(
                    f"<b>Неправильный ввод! Введите целое отрицательное число!</b> ❌",
                    parse_mode=ParseMode.HTML,
                    )
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в FSM [Form.removing_price_waiting (admin_keyboard.py)] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)

    @dp.message(Form.expense_amount_waiting)
    async def expense_amount_process(message: Message, state: FSMContext):
        try:
            await message.delete()
            amount = message.text

            if amount.isdigit():
                amount = int(amount)
                current_balance = await get_current_balance()

                if amount <= current_balance:
                    data = await state.get_data()
                    expense_type = data.get("expense_type")
                    await state.update_data(expense_amount=amount)
                    
                    await message.answer(f"<b>Вы потратили {amount}₽ на {expense_type}</b>\nВерно?", parse_mode=ParseMode.HTML, reply_markup=get_confirm_expense_keyboard())
                else:
                    await message.answer("<b>Ошибка!\nНедостаточно средств на балансе!</b> 💰\n<b>Обратитесь к админу!</b> ⚠️\n/start", parse_mode=ParseMode.HTML)
            else:
                await message.answer(
                    f"<b>Неправильный ввод! Введите целое положительное число!</b> ❌",
                    parse_mode=ParseMode.HTML,
                    )
        except Exception as e:
            logger.exception(f"[{message.from_user.id}] Ошибка в FSM [Form.expense_amount_waiting (admin_keyboard.py)] [{e}]")
            await message.answer("⚠️ <b>Что-то пошло не так. Попробуйте позже.</b>", parse_mode=ParseMode.HTML)