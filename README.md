# Проект Lyceum

Данный проект создан на Django версии 5.2.* и содержит три приложения:
- **homepage**
- **catalog**
- **about**

## Установка и запуск в dev-режиме

Проект предназначен для запуска в режиме разработки (dev), который характеризуется расширенной отладочной информацией и пониженной безопасностью. Обратите внимание, что запуск проекта в dev-режиме **не рекомендуется** для продакшена.

### Шаг 1. Клонирование репозитория

```bash
git clone https://gitlab.crja72.ru/django/2025/spring/course/students/307818-EugeneINNO-course-1340.git
cd lyceum
```
### Шаг 2. Создание и активация виртуального окружения
```
python3 -m venv venv
source venv/bin/activate 
```
для Linux/MacOS; на Windows: 
```
venv\Scripts\activate.ps1 # для PowerShell 
venv\Scripts\activate.bat # для CMD
```
### Шаг 3. Установка зависимостей
```
pip install -r requirements.txt
```
### Шаг 4. Запуск сервера разработки
```
python manage.py runserver
```
После запуска сервер будет доступен по адресу http://127.0.0.1:8000/.