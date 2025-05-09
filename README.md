# MosPolytech-schedule-bot ![image](https://github.com/user-attachments/assets/295305e3-acc2-4a2f-9ea4-9951aa0123ef)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13.3-yellow?logo=python&logoColor=white)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
## 📝 Описание
Официальный Telegram-бот для студентов Московского Политехнического Университета (МПУ). Бот предоставляет удобный доступ к актуальному расписанию прямо в Telegram.

**✨ Возможности:**
- 🕒 Расписание занятий и экзаменов
- 🔍 Поиск по группам и преподавателям
- 📅 Автоматическое обновление данных
- 🤖 Удобный интерфейс в Telegram
## 📌 Обзор проекта
Telegram-бот для работы с расписанием. Проект состоит из трех основных модулей:
- `api/` - работа с внешними API и данными
- `bot/` - основная логика бота
- `config/` - настройки приложения
  

## Команды
- `/start` - приветственное сообщение
- `/чепопарам` -  получить расписание
- `/чепопарам [группа]` - получить расписание конкретной группы
## Установка и запуск
1. Установка зависимостей
pip install -r requirements.txt  или
pip install python-telegram-bot requests
2. Создать файл .env м написать там свой тг токен TELEGRAM_TOKEN='Ваш токен', который можно узнать у тг бота @BotFather
3. Запустить бота:
python -m bot.telegram_bot или запустить telegram_bot.py

## Сайт с опсианием телеграмм бота
https://m0nkl.github.io/




## Разработчики
[Oleg Maslennikov](https://github.com/M0nkl) <br>
[Komarov Egor](https://github.com/pojalustayuidi)
