## Установка

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/GeraPegov/parse_file
cd parse-file
```

### 2. Создайте виртуальное окружение
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Установка зависимостей
```bash 
pip install -r requirements.txt
```

### 4. Настройте переменные окружения
```bash
cp .env.example .env

POSTGRES_USER=user_name
POSTGRES_PASSWORD=password_name

#host and port дефолтные для локального подключения
ADMIN_DB_URL=postgresql+asyncpg://user_name:password_name@localhost:5432/postgres
PROD_DB_URL=postgresql+asyncpg://user_name:password_name@localhost:5432/tourism
TEST_DB_URL=postgresql+asyncpg://user_name:your_password@localhost:5432/testtourism
```

## Настройка базы данных

### 1. Запустите сервер PostgreSQL 


### 2. Инициализируйте таблицы
```bash 
python scripts/init_db.py
```

Этот скрипт создаст:
- Продакшн БД: `tourism`
- Тестовую БД: `testtourism`

### 3. Примените миграции 
```bash 
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```
Создаст таблицу 'tourism' модели TourismData

### Запуск тестов
```bash
pytest
```
Возможно придется перезайти в окружение
```bash
deactivate
source .venv/bin/activate
```
## Запуск приложения
Убедитесь что вы в директории проекта
```bash
uvicorn main:app --reload
```
Приложение будет доступно по адресу: **http://127.0.0.1:8000/**



## Использование


## 1. Загрузка данных

1. Откройте **http://localhost:8000**
2. Нажмите **"Выбрать файл"** и загрузите CSV файл
3. Нажмите **"Загрузить данные"**

Данные загружаются около 2 минут
Будет JSON-ответ {'status': success}
### 2. Получение аналитики

1. Нажмите **"Анализ данных"**
2. Скачается JSON файл `tourism_analysis.json` с отчётом

### 3. Очистка данных

1. Нажмите **"Очистить базу"**
2. Подтвердите действие
3. Все данные будут удалены из БД

---