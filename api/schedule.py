import requests
import json
import logging
from typing import Dict, Any
from datetime import datetime, timedelta
import re
from config.settings import BASE_URL, API_URL, HEADERS, SCHEDULE_TIMES, WEEK_DAYS

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Словарь для преобразования русских названий месяцев
MONTHS_RU = {
    "янв": 1, "фев": 2, "мар": 3, "апр": 4, "май": 5, "июн": 6,
    "июл": 7, "авг": 8, "сен": 9, "окт": 10, "ноя": 11, "дек": 12
}


def fetch_schedule(group: str, session: str = "0") -> Dict[str, Any]:
    """
    Получает расписание для заданной группы через API rasp.dmami.ru.
    """
    params = {"group": group, "session": session}
    session = requests.Session()

    try:
        logger.info("Получаем куки с главной страницы...")
        response = session.get(BASE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()

        logger.info(f"Запрашиваем расписание для группы {group}...")
        response = session.get(API_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "")
        logger.info(f"Content-Type ответа: {content_type}")

        if "application/json" not in content_type.lower():
            logger.error("Сервер вернул не JSON:")
            logger.error(response.text)
            raise ValueError("Ожидался JSON, но получен другой формат")

        data = response.json()
        logger.debug(f"Полученные данные: {data}")

        if isinstance(data, str):
            logger.warning("Данные получены как строка, пробуем распарсить ещё раз...")
            data = json.loads(data)

        logger.info(f"Полные данные API: {json.dumps(data, ensure_ascii=False, indent=2)}")
        return data

    except requests.HTTPError as e:
        logger.error(f"HTTP ошибка: {e} (Код: {response.status_code})")
        logger.error(f"Текст ответа: {response.text}")
        raise
    except ValueError as e:
        logger.error("Ошибка парсинга JSON:")
        logger.error(response.text)
        raise
    except requests.RequestException as e:
        logger.error(f"Ошибка запроса: {e}")
        raise
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}")
        raise


def is_date_range_valid(dts: str, current_date: datetime) -> bool:
    """
    Проверяет, является ли диапазон дат в поле dts актуальным для текущей даты.
    """
    logger.info(f"Проверка диапазона дат: '{dts}'")
    if not dts or dts == "Не указано":
        logger.info("Даты не указаны, занятие считается актуальным")
        return True

    try:
        date_parts = [part.strip() for part in dts.split("-")]
        current_year = current_date.year

        def parse_date(date_str: str) -> datetime:
            match = re.match(r"(\d{1,2})\s+([а-яА-Я]+)", date_str, re.IGNORECASE)
            if not match:
                raise ValueError(f"Некорректный формат даты: {date_str}")

            day, month_str = match.groups()
            month_str = month_str.lower()[:3]
            if month_str not in MONTHS_RU:
                raise ValueError(f"Неизвестный месяц: {month_str}")

            month = MONTHS_RU[month_str]
            day = int(day)
            return datetime(current_year, month, day)

        if len(date_parts) == 1:
            single_date = parse_date(date_parts[0])
            is_valid = single_date.date() == current_date.date()
            logger.info(
                f"Одиночная дата: {single_date.date()}, текущая дата: {current_date.date()}, актуально: {is_valid}")
            return is_valid
        elif len(date_parts) == 2:
            start_str, end_str = date_parts
            start_date = parse_date(start_str)
            end_date = parse_date(end_str)

            if end_date < start_date:
                end_date = end_date.replace(year=current_year + 1)

            is_valid = start_date.date() <= current_date.date() <= end_date.date()
            logger.info(
                f"Диапазон: {start_date.date()} - {end_date.date()}, текущая дата: {current_date.date()}, актуально: {is_valid}")
            return is_valid
        else:
            logger.warning(f"Некорректный формат диапазона дат: '{dts}'")
            return False

    except Exception as e:
        logger.error(f"Ошибка парсинга диапазона дат '{dts}': {e}")
        return False


def format_schedule(data: Dict[str, Any], selected_day: str = None) -> str:
    """
    Форматирует данные расписания в читаемый текстовый вид.
    """
    if not isinstance(data, dict):
        logger.error(f"Ожидался словарь, но получен: {type(data)}")
        raise ValueError("Данные должны быть словарем")

    if data.get("status") != "ok":
        return "Ошибка: расписание не найдено."

    grid = data.get("grid", {})
    if not grid:
        return "Расписание пустое."

    formatted = []
    current_date = datetime.now()
    logger.info(f"Форматирование расписания для даты: {current_date.date()}")
    days_to_process = [selected_day] if selected_day else grid.keys()

    for day in days_to_process:
        pairs = grid.get(day, {})
        if not pairs or not any(pairs.values()):
            logger.info(f"День {day} пустой, пропускаем")
            continue

        day_name = WEEK_DAYS.get(day, f"День {day}")
        formatted.append(f"📅 {day_name}:")
        for pair_num, lessons in pairs.items():
            logger.info(f"Обработка пары {pair_num}, lessons: {lessons}")
            if not lessons:
                logger.info(f"Пара {pair_num} пустая, пропускаем")
                continue

            valid_lessons = []
            for lesson in lessons:
                if not isinstance(lesson, dict):
                    logger.error(f"Ожидался словарь для занятия, но получен: {type(lesson)}, значение: {lesson}")
                    continue

                dts = lesson.get("dts", "Не указано")
                if not is_date_range_valid(dts, current_date):
                    logger.info(f"Пропущено занятие: {lesson.get('sbj', 'Не указано')}, даты: {dts}")
                    continue

                valid_lessons.append(lesson)

            if not valid_lessons:
                logger.info(f"Пара {pair_num} не содержит актуальных занятий, пропускаем")
                continue

            time = SCHEDULE_TIMES.get(pair_num, "N/A")
            formatted.append(f"  🕒 {time} (Пара {pair_num}):")
            for lesson in valid_lessons:
                subject = lesson.get("sbj", "Не указано")
                teacher = lesson.get("teacher", "Не указано")
                location = lesson.get("location", "Не указано")
                lesson_type = lesson.get("type", "Не указано")
                dts = lesson.get("dts", "Не указано")
                logger.info(f"Добавлено занятие: {subject}, даты: {dts}, преподаватель: {teacher}, место: {location}")
                formatted.append(f"    📖 {subject} ({lesson_type})")
                formatted.append(f"    👨‍🏫 {teacher}")
                formatted.append(f"    📍 {location} | 🗓️ {dts}")
            formatted.append("")

        formatted.append("")

    result = "\n".join(formatted) if formatted else "Расписание пустое."
    logger.info(f"Итоговое расписание: {result[:100]}... (длина: {len(result)} символов)")
    return result