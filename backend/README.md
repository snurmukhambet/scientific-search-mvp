# Scientific Search MVP

## Установка
```bash
py -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Настройка
Создайте `.env`:
```
GEMINI_API_KEY=ваш_ключ
```

## Запуск
```bash
python run_server.py
```

## API
- GET / - статус
- POST /api/ask - вопрос Gemini

## Тесты
```bash
pytest
```
