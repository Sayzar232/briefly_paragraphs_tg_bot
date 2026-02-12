# briefly_paragraphs - Telegram bot

Краткий бот для получения кратких изложений параграфов из ресурсов.

Запуск с webhook (рекомендуется для хостинга):

1. Создайте файл `.env` в корне с переменными:

```
TOKEN=ВАШ_TELEGRAM_TOKEN
WEBHOOK_URL=https://your.domain.com
WEBHOOK_PATH=/tg_webhook
ADMIN_TOKEN=секрет_для_админки
APP_HOST=0.0.0.0
APP_PORT=8000
DATABASE_NAME=users.db
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Запустите приложение:

```bash
python main.py
```

Примечания:
- Админ-панель доступна по `GET /admin?token=...` и возвращает количество пользователей.
- Для локальной разработки можно использовать ngrok для проброса HTTPS и указать `WEBHOOK_URL` на ngrok URL.
