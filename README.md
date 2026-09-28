# GOIT Web HW #8

## Що реалізовано

### Частина 1
- MongoDB Atlas + MongoEngine
- моделі `Author` та `Quote`
- `Quote.author` — `ReferenceField(Author)`
- імпорт `authors.json` та `quotes.json`
- пошук:
  - `name:Steve Martin`
  - `name:st`
  - `tag:life`
  - `tag:li`
  - `tags:life,live`
  - `exit`
- Redis-кеш для `name:` та `tag:`

### Частина 2
- MongoDB модель `Contact`
- RabbitMQ
- `producer.py` генерує Faker-контакти та кладе їх ObjectID у черги
- `consumer.py` обробляє email-чергу
- додатково:
  - телефон
  - preferred channel: `email` / `sms`
  - `consumer_email.py`
  - `consumer_sms.py`
  - окремі RabbitMQ черги

## 1. Встановлення

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Створи `.env` на основі `.env.example`.

## 2. MongoDB Atlas

Створи кластер MongoDB Atlas та встав URI у `.env`:

```env
MONGODB_URI=mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/goit_hw_08?retryWrites=true&w=majority
```

Якщо пароль містить спеціальні символи, їх потрібно URL-encode.

## 3. Redis та RabbitMQ

Найпростіше запустити через Docker:

```powershell
docker compose up -d
```

Перевір:

```powershell
docker ps
```

## 4. Імпорт авторів та цитат

```powershell
python seed_quotes.py
```

## 5. Пошук

```powershell
python search_quotes.py
```

Приклади:

```text
name:Steve Martin
name:st
tag:life
tag:li
tags:life,live
exit
```

## 6. RabbitMQ

У першому PowerShell:

```powershell
python consumer.py
```

У другому:

```powershell
python producer.py
```

Для додаткового завдання можна окремо запустити:

```powershell
python consumer_email.py
python consumer_sms.py
```

і потім:

```powershell
python producer.py
```

За замовчуванням producer створює 10 контактів. Кількість можна змінити:

```powershell
python producer.py 20
```
