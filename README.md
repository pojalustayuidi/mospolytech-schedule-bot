# MosPolytech-schedule-bot ![image](https://github.com/user-attachments/assets/295305e3-acc2-4a2f-9ea4-9951aa0123ef)

![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13.3-yellow?logo=python&logoColor=white)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

# Перейти в бота[![Перейти в бота](https://img.shields.io/badge/-@MospolytechShedule__Bot-0088CC?style=for-the-badge&logo=telegram)](https://t.me/MospolytechShedule_Bot)
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

## 🛠 Установка и настройка
### Предварительные требования
- Установленный [Python 3.13.3](https://www.python.org/downloads/)
- Аккаунт в Telegram и токен бота от [@BotFather](https://t.me/BotFather)
- Учетная запись GitHub (для клонирования репозитория)

### Пошаговая инструкция

1. **Клонирование репозитория**
``bash
git clone https://github.com/M0nkl/MosPolytech-schedule-bot.git``
``cd MosPolytech-schedule-bot ``
2. **Создание виртуального окружения**
``python -m venv venv``
3. **Установка зависимостей**
``pip install -r requirements.txt `` или
``pip install python-telegram-bot requests``
4. **Настройка конфигурации
Создайте файл .env в корне проекта:**
``TELEGRAM_TOKEN="ваш_токен"``
5. **Запуск бота**
  `` python -m bot.telegram_bot``


## Сайт с опсианием телеграмм бота
https://m0nkl.github.io/




## Разработчики
- **[Олег Масленников](https://github.com/M0nkl)** 
- **[Егор Комаров](https://github.com/pojalustayuidi)** 
