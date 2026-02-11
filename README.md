# Django Booking System

Система бронирования переговорных комнат на Django REST Framework.

## Установка

```bash
git clone https://github.com/dam908/Django.git
cd Django
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```

## API Endpoints

- `GET /rooms/` — список комнат
- `GET /rooms/{id}/bookings/` — брони комнаты
- `GET /rooms/free/?start_time=<datetime>&end_time=<datetime>` — свободные комнаты
- `POST /bookings/` — создать бронь

## Пример запроса

```bash
curl -X POST http://127.0.0.1:8000/bookings/ \
  -H "Content-Type: application/json" \
  -d '{
    "room": 1,
    "user_name": "Иван",
    "start_time": "2026-02-11T10:00:00Z",
    "end_time": "2026-02-11T12:00:00Z"
  }'
```

## Бизнес-логика

- Запрет пересечений бронирований
- Максимум 3 активные брони на пользователя
- Валидация времени (end_time > start_time)
- Логирование срочных броней (< 10 минут)

## Модели

**Room:** name, capacity, has_projector  
**Booking:** room, user_name, start_time, end_time, created_at

## Автор

dam908
