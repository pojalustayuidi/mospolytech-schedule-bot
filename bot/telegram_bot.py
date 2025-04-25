import sys
import os
import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
# Проверяем путь
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
try:
    from api.schedule import fetch_schedule, format_schedule
except ModuleNotFoundError as e:
    print(f"Ошибка импорта: {e}")
    raise
from config.settings import TELEGRAM_TOKEN, WEEK_DAYS

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Инициализация бота и диспетчера с явным хранилищем FSM
bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Определяем состояния для FSM
class ScheduleForm(StatesGroup):
    waiting_for_group = State()

def create_day_buttons() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for day_num, day_name in WEEK_DAYS.items():
        button = InlineKeyboardButton(
            text=day_name,
            callback_data=f"day_{day_num}"
        )
        keyboard.inline_keyboard.append([button])
    return keyboard

@dp.message(Command("start"))
async def start(message: Message):
    """
    Обработчик команды /start.
    Отправляет приветственное сообщение.
    """
    user = message.from_user
    await message.reply(
        f"Привет, {user.first_name}! 👋\n"
        "Я бот, который поможет тебе узнать расписание Московского Политеха.\n"
        "Используй команду /schedule, чтобы ввести номер группы, или /schedule [группа] для быстрого запроса.\n"
        "Пример: /чепопарам 241-335"
    )

@dp.message(Command("чепопарам"))
async def schedule(message: Message, state: FSMContext):
    """
    Обработчик команды /чепопарам   .
    Запрашивает расписание для группы или просит ввести номер группы.
    """
    args = message.text.split(maxsplit=1)

    if len(args) > 1:
        group = args[1]
        await process_schedule(message, group, state)
    else:
        await message.reply("Пожалуйста, введи номер группы (например, 241-335):")
        await state.set_state(ScheduleForm.waiting_for_group)

@dp.message(ScheduleForm.waiting_for_group)
async def process_group(message: Message, state: FSMContext):
    """
    Обработчик ввода группы в состоянии ожидания.
    """
    group = message.text.strip()
    await process_schedule(message, group, state)

async def process_schedule(message: Message, group: str, state: FSMContext):
    """
    Получает расписание для указанной группы и отправляет клавиатуру для выбора дня.
    """
    try:
        if not group.replace("-", "").isdigit():
            await message.reply("Номер группы должен содержать только цифры и дефис (например, 241-335).")
            return

        schedule_data = fetch_schedule(group=group, session="0")
        logger.info(f"Расписание успешно получено через API для группы {group}.")
        logger.info(f"Контекст: user_id={message.from_user.id}, chat_id={message.chat.id}")

        await state.update_data(schedule_data=schedule_data, group=group)
        logger.info(f"Данные сохранены в FSM: group={group}, schedule_data_keys={list(schedule_data.keys())}")

        if not schedule_data.get("grid"):
            await message.reply("Не удалось найти расписание для этой группы.")
            return

        await message.reply(
            f"Выбери день недели для группы {group}:",
            reply_markup=create_day_buttons()
        )

    except Exception as e:
        logger.error(f"Ошибка при получении расписания для группы {group}: {e}")
        await message.reply("Произошла ошибка при получении расписания. Попробуй позже.")

@dp.callback_query(lambda c: c.data.startswith("day_"))
async def process_day_selection(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик нажатия на кнопку дня недели.
    """
    try:
        day_num = callback.data.split("_")[1]
        day_name = WEEK_DAYS.get(day_num, f"День {day_num}")

        logger.info(f"Контекст: user_id={callback.from_user.id}, chat_id={callback.message.chat.id}")
        user_data = await state.get_data()
        logger.info(f"Извлечены данные из FSM: {user_data}")
        schedule_data = user_data.get("schedule_data")
        group = user_data.get("group")

        if not group:
            logger.warning("Группа не найдена в FSM")
            await callback.message.reply("Группа не указана. Пожалуйста, запроси расписание заново с помощью /schedule.")
            await callback.answer()
            return

        if not schedule_data:
            logger.warning(f"Данные расписания отсутствуют для группы {group}, запрашиваем заново")
            try:
                schedule_data = fetch_schedule(group=group, session="0")
                await state.update_data(schedule_data=schedule_data, group=group)
                logger.info(f"Расписание успешно получено повторно для группы {group}")
            except Exception as e:
                logger.error(f"Ошибка повторного запроса расписания для группы {group}: {e}")
                await callback.message.reply("Не удалось обновить расписание. Попробуй запросить заново с помощью /schedule.")
                await callback.answer()
                return

        formatted_schedule = format_schedule(schedule_data, selected_day=day_num)
        logger.info(f"Расписание отформатировано для группы {group}, день {day_name}.")

        if not formatted_schedule or formatted_schedule == "Расписание пустое.":
            await callback.message.reply(f"На {day_name} нет актуальных пар для группы {group}.")
            await callback.answer()
            return

        max_length = 4000
        parts = []
        current_part = f"📅 {day_name} (группа {group}):\n\n"
        for line in formatted_schedule.split("\n"):
            if len(current_part) + len(line) + 1 <= max_length:
                current_part += line + "\n"
            else:
                parts.append(current_part)
                current_part = line + "\n"
        if current_part:
            parts.append(current_part)

        for part in parts:
            try:
                await callback.message.reply(part)
            except TelegramBadRequest as e:
                logger.error(f"Ошибка отправки части сообщения: {e}")
                await callback.message.reply("Ошибка при отправке расписания. Попробуй позже.")
                return

        await callback.answer()

    except Exception as e:
        logger.error(f"Ошибка при обработке выбора дня: {e}")
        await callback.message.reply("Произошла ошибка. Попробуй позже.")
        await callback.answer()

async def main():
    """
    Основная функция для запуска Telegram-бота.
    """
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_TOKEN не задан в .env файле.")
        sys.exit(1)

    logger.info("Запускаем Telegram-бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())