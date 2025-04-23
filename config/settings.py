import os

from dotenv import load_dotenv

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
# API rasp.dmami.ru
BASE_URL = "https://rasp.dmami.ru/"
API_URL = f"{BASE_URL}site/group"
GROUP = "241-335"
SESSION = "0"

SCHEDULE_TIMES = {
    "1": "09:00–10:30",
    "2": "10:40–12:10",
    "3": "12:20–13:50",
    "4": "14:30–16:00",
    "5": "16:10–17:40",
    "6": "17:50–19:20",
    "7": "19:30–21:00",
}
WEEK_DAYS = {
    "1": "Понедельник",
    "2": "Вторник",
    "3": "Среда",
    "4": "Четверг",
    "5": "Пятница",
    "6": "Суббота",
}

# Заголовки для запроса
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": BASE_URL,
}