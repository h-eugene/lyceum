## Установка и запуск в dev-режиме

### 1. Клонирование репозитория
```sh
git clone https://gitlab.crja72.ru/django/2025/spring/course/students/175774-lntckkk-course-1340.git
cd lyceum
```

### 2. Создание и активация виртуального окружения
```sh
python3 -m venv venv
source venv/bin/activate # linux/MacOS, for Windows venv/Scripts/activate.ps1 or venv/Scripts/activate.bat
```

### 3. Установка зависимостей
```sh
pip install -r requirements.txt
```

### 4. Запуск dev-сервера
Запускаем сервер Django в режиме разработки (**DEBUG=True** в `settings.py`):
```sh
python manage.py runserver
```
Сервер будет доступен по адресу: **http://127.0.0.1:8000/**