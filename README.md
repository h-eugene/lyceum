# Lyceum

## Установка и запуск в dev-режиме

### **1️⃣ Клонирование репозитория**
```sh
git clone https://gitlab.crja72.ru/django/2025/spring/course/students/175774-lntckkk-course-1340.git
cd lyceum
```

---

### **2️⃣ Создание и активация виртуального окружения**
```sh
python3 -m venv venv
source venv/bin/activate  # Linux/MacOS
# Для Windows:
# venv\Scripts\activate.ps1 (PowerShell)
# venv\Scripts\activate.bat (CMD)
```

---

### **3️⃣ Настройка `.env`**
Создайте `.env` в корневой папке проекта:

```ini
SECRET_KEY=django-insecure-1234567890abcdef
DEBUG=True
ALLOWED_HOSTS=localhost 127.0.0.1
```

⚠️ **Важно:** Файл `.env` **не должен попадать в репозиторий!** Он уже добавлен в `.gitignore`.

---

### **4️⃣ Установка зависимостей**
#### **Продакшн (основные зависимости)**
```sh
pip install -r requirements/prod.txt
```
#### **Для разработки (с доп. инструментами)**
```sh
pip install -r requirements/dev.txt
```
#### **Для тестов**
```sh
pip install -r requirements/test.txt
```

---

### **5️⃣ Запуск dev-сервера**
Запускаем сервер Django в режиме разработки (**DEBUG=True** в `.env`):
```sh
python manage.py runserver
```
Сервер будет доступен по адресу: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

