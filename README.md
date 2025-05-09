# MosPolytech-schedule-bot\
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
## Описание
Данный бот предназначен для студентов Москвоского Политехнического Университета (МПУ).  С его помощью студенты могут
- узнать расписание пар
- узнать расписание зачетов <br>
- Узнать до какого периода какая то дисциплина
- Удобное внедрение телеграмм бота в свою группу

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
