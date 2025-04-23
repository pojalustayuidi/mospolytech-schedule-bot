# import sys
# import os
# import logging
# import asyncio
# from aiogram import Bot, Dispatcher
# from aiogram.filters import Command
# from aiogram.types import Message
# from api.schedule import fetch_schedule, format_schedule
# from config.settings import TELEGRAM_TOKEN
#
# # Добавляем корневую папку проекта в sys.path
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, project_root)
#
# # Настройка логирования
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s"
# )
# logger = logging.getLogger(__name__)
#
# # Инициализация бота и диспетчера
# bot = Bot(token=TELEGRAM_TOKEN)
# dp = Dispatcher()
#
#
# @dp.message(Command("start"))
# async def start(message: Message):
#     """
#     Обработчик команды /start.
#     Отправляет приветственное сообщение.
#     """
#     user = message.from_user
#     await message.reply(
#         f"Привет, {user.first_name}! 👋\n"
#         "Я бот, который поможет тебе узнать расписание Московского Политеха.\n"
#         "Используй команду /schedule [группа], чтобы получить расписание (по умолчанию 241-335).\n"
#         "Пример: /schedule 241-335"
#     )
#
#
# @dp.message(Command("schedule"))
# async def schedule(message: Message):
#     """
#     Обработчик команды /schedule.
#     Получает и отправляет расписание для группы.
#     """
#     # Извлекаем группу из аргументов команды, по умолчанию 241-335
#     args = message.text.split(maxsplit=1)
#     group = args[1] if len(args) > 1 else "241-335"
#
#     try:
#         # Получаем расписание
#         schedule_data = fetch_schedule(group=group, session="0")
#         logger.info(f"Расписание успешно получено через API для группы {group}.")
#
#         # Форматируем расписание
#         formatted_schedule = format_schedule(schedule_data)
#         logger.info("Расписание отформатировано.")
#
#         # Отправляем расписание пользователю
#         if formatted_schedule:
#             await message.reply(formatted_schedule)
#         else:
#             await message.reply("Не удалось отформатировать расписание.")
#
#     except Exception as e:
#         logger.error(f"Ошибка при получении расписания для группы {group}: {e}")
#         await message.reply("Произошла ошибка при получении расписания. Попробуй позже.")
#
#
# async def main():
#     """
#     Основная функция для запуска Telegram-бота.
#     """
#     if not TELEGRAM_TOKEN:
#         logger.error("TELEGRAM_TOKEN не задав .env файле.")
#         sys.exit(1)
#
#     logger.info("Запускаем Telegram-бота...")
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     asyncio.run(main())