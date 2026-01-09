"""
OAuth 2.0 Authorization Code Flow клиент для GitHub
"""

from requests_oauthlib import OAuth2Session
import os
import json
from urllib.parse import urlparse, parse_qs

# Конфигурация
CLIENT_ID = os.environ.get("GITHUB_CLIENT_ID", "Ov23li4caecKrhljDjpZ")
CLIENT_SECRET = os.environ.get(
    "GITHUB_CLIENT_SECRET", "e70d39937db081cf3ba000ac690782f3929b0aa3"
)
REDIRECT_URI = "http://localhost:3000"
AUTHORIZATION_BASE_URL = "http://localhost:3000/auth/github/callback"
TOKEN_URL = "https://github.com/login/oauth/access_token"

# Права доступа (scopes)
SCOPES = [
    "read:user",
    "user:email",
]


def main():
    """Основная функция OAuth клиента"""

    print("=== OAuth 2.0 Authorization Code Flow ===")
    print(f"Client ID: {CLIENT_ID[:10]}...")

    # Проверка наличия client_id и client_secret
    if CLIENT_ID == "ваш_client_id_здесь" or not CLIENT_ID:
        print("\n⚠️  ВНИМАНИЕ: Установите CLIENT_ID и CLIENT_SECRET!")
        print("Способы установки:")
        print("1. Замените значения в коде")
        print("2. Установите переменные окружения:")
        print("   export GITHUB_CLIENT_ID='ваш_id'")
        print("   export GITHUB_CLIENT_SECRET='ваш_secret'")
        print("3. Создайте файл .env с переменными")
        return

    # 1. Создание OAuth сессии
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)

    # 2. Генерация URL для авторизации
    authorization_url, state = oauth.authorization_url(
        AUTHORIZATION_BASE_URL, state="random_state_string"  # Защита от CSRF
    )

    print(f"\n1. Перейдите по ссылке для авторизации:")
    print(f"   {authorization_url}")
    print(f"\n   State (для проверки): {state}")

    # 3. Получение redirect URL от пользователя
    print("\n" + "=" * 50)
    print("2. После авторизации GitHub перенаправит вас на:")
    print(f"   {REDIRECT_URI}")
    print("\n3. Скопируйте ПОЛНЫЙ URL из адресной строки браузера")
    print(
        "   Пример: http://localhost:8000/callback?code=abc123&state=random_state_string"
    )

    redirect_response = input("\nВставьте полный URL перенаправления: ").strip()

    # 4. Извлечение state из URL для проверки
    parsed = urlparse(redirect_response)
    query_params = parse_qs(parsed.query)
    returned_state = query_params.get("state", [None])[0]

    if returned_state != state:
        print(
            f"⚠️  Ошибка проверки state! Ожидалось: {state}, получено: {returned_state}"
        )
        return

    # 5. Обмен кода авторизации на токен доступа
    print("\n4. Обмен кода на токен доступа...")
    try:
        token = oauth.fetch_token(
            TOKEN_URL,
            authorization_response=redirect_response,
            client_secret=CLIENT_SECRET,
            headers={"Accept": "application/json"},
        )

        print("✅ Токен успешно получен!")

        with open("token.json", "w") as f:
            json.dump(token, f, indent=2)
        print("   Токен сохранен в token.json")

    except Exception as e:
        print(f"❌ Ошибка при получении токена: {e}")
        return

    # 6. Использование токена для доступа к API
    print("\n5. Запрос данных пользователя...")
    try:

        response = oauth.get("https://api.github.com/user")

        if response.status_code == 200:
            user_data = response.json()
            print("\n✅ Данные пользователя получены!")
            print(f"   Имя: {user_data.get('name', 'Не указано')}")
            print(f"   Логин: {user_data.get('login')}")
            print(f"   Email: {user_data.get('email', 'Скрыт')}")
            print(f"   ID: {user_data.get('id')}")
            print(f"   URL профиля: {user_data.get('html_url')}")

            # Дополнительный запрос email (если scope включает user:email)
            if "user:email" in SCOPES:
                emails_response = oauth.get("https://api.github.com/user/emails")
                if emails_response.status_code == 200:
                    emails = emails_response.json()
                    primary_email = next((e for e in emails if e["primary"]), None)
                    if primary_email:
                        print(f"   Основной email: {primary_email['email']}")
        else:
            print(f"   Ошибка запроса: {response.status_code}")
            print(f"   Ответ: {response.text}")

    except Exception as e:
        print(f"Ошибка при запросе данных: {e}")


def test_quick_start():
    """Быстрый старт для тестирования (если уже есть токен)"""
    print("\n=== Быстрая проверка существующего токена ===")

    try:
        with open("token.json", "r") as f:
            token = json.load(f)

        oauth = OAuth2Session(CLIENT_ID, token=token)

        response = oauth.get("https://api.github.com/user")
        print(f"Статус: {response.status_code}")
        print(f"Пользователь: {response.json().get('login')}")

    except FileNotFoundError:
        print("Файл token.json не найден. Выполните полную авторизацию.")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()

    # test_quick_start()