# Geo Points Backend

Backend-приложение на Django для работы с географическими точками и сообщениями в постапокалиптическом мире («Тихий Сдвиг»).  
Позволяет создавать точки на карте, оставлять сообщения к ним и получать данные через REST API.

## Технологии

- Python 3.14
- Django 5.1
- Django REST Framework
- GeoDjango + Spatialite (SQLite)
- Basic Authentication

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone <ваш-репозиторий>
   cd <имя-папки>

Создайте и активируйте виртуальное окружение:Bashpython -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
Установите зависимости:Bashpip install django==5.1 djangorestframework
Важно для Windows: установка GDAL
Скачайте wheel-файл с https://github.com/cgohlke/geospatial-wheels/releases
(выберите версию для вашей Python, например GDAL-3.11.4-cp314-cp314-win_amd64.whl)Bashpip install путь/к/GDAL-3.11.4-cp314-cp314-win_amd64.whl
Настройте пути к библиотекам в config/settings.py (добавьте в конец файла):PythonGDAL_LIBRARY_PATH = r'C:\Users\...\venv\Lib\site-packages\osgeo\gdal311.dll'
GEOS_LIBRARY_PATH = r'C:\Users\...\venv\Lib\site-packages\osgeo\geos_c.dll'
SPATIALITE_LIBRARY_PATH = 'mod_spatialite'
Примените миграции и создайте суперюзера:Bashpython manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
Запустите сервер:Bashpython manage.py runserver

Основные эндпоинты
Все эндпоинты защищены авторизацией (Basic Auth).
1. Создание точки на карте
POST /api/points/
Тело запроса (JSON):
JSON{
  "title": "Точка в Франкфурте",
  "longitude": 8.6821,
  "latitude": 50.1109
}
2. Создание сообщения к точке
POST /api/messages/
Тело запроса (JSON):
JSON{
  "point": 1,                     // ID существующей точки
  "text": "Здесь можно отдохнуть. Мертвецы далеко."
}
3. Получение сообщений в радиусе (поиск по гео)
GET /api/messages/search/?latitude=50.11&longitude=8.68&radius=10
Возвращает список сообщений в указанном радиусе (по умолчанию 5 км).
4. Список всех точек
GET /api/points/
Авторизация
Все запросы требуют Basic Authentication.
Пример в curl:
Bashcurl -u iskatel1:secret123 \
     -H "Content-Type: application/json" \
     -d '{"point": 1, "text": "Тихо, припасы рядом"}' \
     http://127.0.0.1:8000/api/messages/
