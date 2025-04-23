import requests
import json
import logging
from typing import Dict, Any
from config.settings import BASE_URL, API_URL, HEADERS, SCHEDULE_TIMES, WEEK_DAYS

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def fetch_schedule(group: str, session: str = "0") -> Dict[str, Any]:
    """
    Получает расписание для заданной группы через API rasp.dmami.ru.

    Args:
        group (str): Номер группы (например, "241-335").
        session (str): Идентификатор сессии (например, "0").

    Returns:
        Dict[str, Any]: Данные расписания в формате JSON.

    Raises:
        requests.HTTPError: Если запрос завершился с ошибкой HTTP.
        ValueError: Если ответ не в формате JSON.
    """
    params = {"group": group, "session": session}
    session = requests.Session()

    try:
        # Получаем куки с главной страницы
        logger.info("Получаем куки с главной страницы...")
        response = session.get(BASE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()

        # Запрос к API
        logger.info(f"Запрашиваем расписание для группы {group}...")
        response = session.get(API_URL, params=params, headers=HEADERS, timeout=10)
        response.raise_for_status()

        # Проверяем заголовки ответа
        content_type = response.headers.get("Content-Type", "")
        logger.info(f"Content-Type ответа: {content_type}")

        # Проверяем, что получили JSON
        if "application/json" not in content_type.lower():
            logger.error("Сервер вернул не JSON:")
            logger.error(response.text)
            raise ValueError("Ожидался JSON, но получен другой формат")

        # Парсим JSON
        data = response.json()
        logger.debug(f"Полученные данные: {data}")

        # Если данные — строка, пробуем распарсить ещё раз
        if isinstance(data, str):
            logger.warning("Данные получены как строка, пробуем распарсить ещё раз...")
            data = json.loads(data)

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

def format_schedule(data: Dict[str, Any], selected_day: str = None) -> str:
    """
    Форматирует данные расписания в читаемый текстовый вид.

    Args:
        data (Dict[str, Any]): Данные расписания из API.
        selected_day (str, optional): Номер дня недели для отображения (например, "1").

    Returns:
        str: Отформатированное расписание.
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
    days_to_process = [selected_day] if selected_day else grid.keys()

    for day in days_to_process:
        pairs = grid.get(day, {})
        if not pairs or not any(pairs.values()):  # Пропускаем дни без пар
            continue

        # Используем название дня недели из WEEK_DAYS
        day_name = WEEK_DAYS.get(day, f"День {day}")
        formatted.append(f"📅 {day_name}:")
        for pair_num, lessons in pairs.items():
            if not lessons:  # Пропускаем пустые пары
                continue

            time = SCHEDULE_TIMES.get(pair_num, "N/A")
            formatted.append(f"  🕒 {time} (Пара {pair_num}):")
            for lesson in lessons:
                if not isinstance(lesson, dict):
                    logger.error(f"Ожидался словарь для занятия, но получен: {type(lesson)}, значение: {lesson}")
                    continue

                subject = lesson.get("sbj", "Не указано")
                teacher = lesson.get("teacher", "Не указано")
                location = lesson.get("location", "Не указано")
                lesson_type = lesson.get("type", "Не указано")
                dts = lesson.get("dts", "Не указано")
                formatted.append(f"    📖 {subject} ({lesson_type})")
                formatted.append(f"    👨‍🏫 {teacher}")
                formatted.append(f"    📍 {location} | 🗓️ {dts}")
            formatted.append("")  # Пустая строка между парами
        formatted.append("")  # Пустая строка между днями

    return "\n".join(formatted) if formatted else "Расписание пустое."