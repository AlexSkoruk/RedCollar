# RedCollar

API для работы с географическими точками и сообщениями к ним.

Проект позволяет создавать точки на карте, оставлять к ним сообщения и искать точки/сообщения в заданном радиусе.

## Возможности

- Полный CRUD для точек (создание, просмотр, обновление, удаление)
- Создание сообщений к точкам
- Поиск точек в радиусе (в километрах)
- Поиск сообщений в радиусе (в километрах)
- Автоматическое определение автора сообщения
- Хранение координат в формате WGS 84 (SRID 4326)

## Технологии

- **Python 3.12+**
- **Django 6.0**
- **Django REST Framework**
- **GeoDjango** + SpatiaLite
- **GDAL / GEOS**

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/AlexSkoruk/RedCollar.git
cd RedCollar
```

### 2. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

#### Важно для Windows: установка GDAL

1. Скачайте wheel-файл с https://github.com/cgohlke/geospatial-wheels/releases
   (выберите версию под вашу Python, например `GDAL-3.11.4-cp314-cp314-win_amd64.whl`)

2. Установите его:

```bash
pip install путь/к/GDAL-3.11.4-cp314-cp314-win_amd64.whl
```

3. Добавьте пути к библиотекам в `config/settings.py` (в конец файла):

```python
GDAL_LIBRARY_PATH = r'C:\Users\...\venv\Lib\site-packages\osgeo\gdal311.dll'
GEOS_LIBRARY_PATH = r'C:\Users\...\venv\Lib\site-packages\osgeo\geos_c.dll'
SPATIALITE_LIBRARY_PATH = 'mod_spatialite'
```

> Замените `C:\Users\...` на актуальный путь к вашему виртуальному окружению.

### 4. Применение миграций

```bash
python manage.py migrate
```

### 5. Создание суперпользователя (опционально)

```bash
python manage.py createsuperuser
```

### 6. Запуск сервера

```bash
python manage.py runserver
```

Сервер будет доступен по адресу: http://127.0.0.1:8000
API: http://127.0.0.1:8000/api/

---

## API Endpoints

Все эндпоинты (кроме корневого) требуют аутентификации.

### Корневой эндпоинт

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/` | Список доступных ресурсов |

### Точки (`/api/points/`)

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/points/` | Список всех точек |
| POST | `/api/points/` | Создать точку |
| GET | `/api/points/{id}/` | Получить точку |
| PUT | `/api/points/{id}/` | Полное обновление |
| PATCH | `/api/points/{id}/` | Частичное обновление |
| DELETE | `/api/points/{id}/` | Удалить точку |
| GET | `/api/points/search/` | Поиск точек в радиусе |

**Параметры поиска точек:**
- `latitude` — широта (обязательно)
- `longitude` — долгота (обязательно)
- `radius` — радиус в **километрах** (по умолчанию 10)

### Сообщения (`/api/messages/`)

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/messages/` | Создать сообщение |
| GET | `/api/messages/search/` | Поиск сообщений в радиусе |

**Параметры поиска сообщений:**
- `latitude` — широта (обязательно)
- `longitude` — долгота (обязательно)
- `radius` — радиус в **километрах** (по умолчанию 5)

---

## Техническое описание

### Модели

**Point**
- `title` — название точки
- `location` — географическая точка (`PointField`, SRID 4326)
- `created_at` — дата создания

**Message**
- `point` — связь с точкой (`ForeignKey`)
- `author` — автор (`ForeignKey` на User, устанавливается автоматически)
- `text` — текст сообщения
- `created_at` — дата создания

### Особенности реализации

- Координаты принимаются и отдаются как отдельные поля `longitude` и `latitude`
- В базе хранится одно поле `location` типа `Point`
- При создании и обновлении точки координаты преобразуются в объект `GEOSGeometry`
- Поиск использует пространственные lookup'ы GeoDjango (`distance_lte`)
- Оба поиска (точки и сообщения) работают в **километрах**
- Автор сообщения устанавливается автоматически из `request.user`

### Структура проекта

```text
RedCollar/
├── config/
├── points/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── point_messages/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── ...
├── manage.py
└── requirements.txt
```
