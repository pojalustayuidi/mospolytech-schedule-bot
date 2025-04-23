import requests
import json

# Настройки API
base_url = "https://rasp.dmami.ru/"
api_url = "https://rasp.dmami.ru/site/group"
params = {"group": "241-335", "session": "0"}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": base_url,
}

session = requests.Session()

try:
    # Получаем куки с главной страницы
    session.get(base_url, headers=headers)

    # Запрос к API
    response = session.get(api_url, params=params, headers=headers)
    response.raise_for_status()  # Проверяем на HTTP-ошибки
    data = response.json()


    print(json.dumps(data, indent=2, ensure_ascii=False))

except requests.HTTPError as e:
    print(f"HTTP ошибка: {e}")
    print(f"Код ответа: {response.status_code}")
    print(f"Текст ответа: {response.text}")
except ValueError:
    print("Ответ не в формате JSON:")
    print(response.text)
except Exception as e:
    print(f"Ошибка: {e}")