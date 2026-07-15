from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import datetime

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота, полученный от BotFather
TOKEN = '8919583440:AAHKm28DtvwRMwkEyet6sZ5cFTWQR_lXNSw'
# IDs каналов и пользователей (замените на актуальные)
CHANNEL_ID = '@WhiHosting' # Ваш канал для подписки
SUPPORT_BOT_UUSERNAME= '@suportWhiteHosting_bot'# Имя пользователя бота пподдержки
# Словарь для хранения информации о пользователях (iid {username, join_date, balance})
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start. Проверяет подписку и предлагает кнопки."""
    user = update.message.from_user
    chat_id = update.message.chat_id

    try:
        # Проверяем, подписан ли пользователь на канал
        chat_member = await context.bot.get_chat_member(CHANNEL_ID, user.id)
        if chat_member.status not in ['member', 'administrator', 'creator']:
            await update.message.reply_text(
                'Пожалуйста, подпишитесь на наш канал, чтобы продолжить: '
                f't.me/{CHANNEL_ID[1:]}',
                reply_markup=inline_keyboard_for_subscription()
            )
            return
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")
        await update.message.reply_text("Произошла ошибка при проверке подписки. Пожалуйста, попробуйте позже.")
        return

    # Если подписан, отправляем приветственное сообщение и кнопки
    await update.message.reply_text(f'Привет, {user.first_name}! Добро пожаловать!')
    await update.message.reply_text(
.id] = {
            'username': user.username,
            'join_date': datetime.datetime.now(),
            'balance': 0
        }

def inline_keyboard_for_subscription():
    """Создает инлайн-клавиатуру для проверки подписки."""
    keyboard = [[InlineKeyboardButton("Проверить подписку", callback_data='check_subscription')]]
    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard():
    """Создает инлайн-клавиатуру основного меню."""
    keyboard = [
        [InlineKeyboardButton("Купить", callback_data='buy')],
        [InlineKeyboardButton("Профиль", callback_data='profile')],
        [InlineKeyboardButton("Поддержка", callback_data='support')]
    ]
    return InlineKeyboardMarkup(keyboard)

def store_keyboard():
    """Создает инлайн-клавиатуру магазина."""
    keyboard = [
        [InlineKeyboardButton("Неделя", callback_data='buy_week')],
        [InlineKeyboardButton("Две недели", callback_data='buy_2_weeks')],
        [InlineKeyboardButton("Три недели", callback_data='buy_3_weeks')],
        [InlineKeyboardButton("Месяц", callback_data='buy_month')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик для всех инлайн-кнопок."""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'check_subscription':
        try:
            chat_member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                await query.edit_message_text(
                    text="Вы еще не подписаны. Пожалуйста, подпишитесь на наш канал: "
                         f"t.me/{CHANNEL_ID[1:]}",
                    reply_markup=inline_keyboard_for_subscription()
                )
            else:
                await query.edit_message_text(text='Спасибо за подписку!')
                await query.message.reply_text(
                    'Выберите действие:',
                    reply_markup=main_menu_keyboard()
                )
        except Exception as e:
            print(f"Ошибка при проверке подписки: {e}")
            await query.edit_message_text("Произошла ошибка при проверке подписки. Пожалуйста, попробуйте позже.")

    elif query.data == 'buy':
        await query.edit_message_text(
            "Выберите товар:",
            reply_markup=store_keyboard()
        )

    elif query.data.startswith('buy_'):
        price = 0
        item_name = ""
        if query.data == 'buy_week':
            price = 100
            item_name = "неделя"
        elif query.data == 'buy_2_weeks':
            price = 180
            item_name = "две недели"
        elif query.data == 'buy_3_weeks':
            price = 250
            item_name = "три недели"
        elif query.data == 'buy_month':
            price = 300
            item_name = "месяц"

        # В реальном приложении здесь была бы логика оплаты
        # Пока просто имитируем покупку и увеличиваем баланс
        user_data[user_id]['balance'] += price
        await query.edit_message_text(
            f"Спасибо за покупку {item_name}! Ваш баланс пополнен. "
            f"Текст: Спасибо за покупку, напишите владельцу бота."
        )
        await query.message.reply_text(
            "Выберите действие:",
            reply_markup=main_menu_keyboard()
        )

    elif_id]['username']}\n"
                f"Зашли: {user_data[user_id]['join_date'].strftime('%Y-%m-%d %H:%M')}\n"
                f"Баланс: {user_data[user_id]['balance']}"
            )
            await query.edit_message_text(profile_info)
        else:
            await query.edit_message_text("Информация о профиле не найдена. Попробуйте команду /start.")
        await query.message.reply_text(
            "Выберите действие:",
            reply_markup=main_menu_keyboard()
        )

    elif query.data == 'support':
        await query.edit_message_text(
            "Свяжитесь с поддержкой:",
            reply_markup=support_keyboard()
        )

def support_keyboard():
    """Создает инлайн-клавиатуру для поддержки."""
    keyboard = [[InlineKeyboardButton("Написать поддержке", url=f"tg://resolve?domain={SUPPORT_BOT_USERNAME[1:]}")]]
    return InlineKeyboardMarkup(keyboard)

def main() -> None:
    """Запускает бота."""
    application = ApplicationBuilder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))

    # Обработчик для всех инлайн-кнопок
    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота
    print("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    main()
