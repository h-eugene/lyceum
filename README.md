# Lyceum
![CI/CD: Проверка стиля](https://gitlab.crja72.ru/django/2025/spring/course/students/307818-EugeneINNO-course-1340/badges/main/pipeline.svg?stage=linting&key_text=Lint)
![CI/CD: Тестирование](https://gitlab.crja72.ru/django/2025/spring/course/students/307818-EugeneINNO-course-1340/badges/main/pipeline.svg?job=django&key_text=Test)

## Установка и запуск в dev-режиме

### **1️⃣ Клонирование репозитория**
```sh
git clone https://gitlab.crja72.ru/django/2025/spring/course/students/307818-EugeneINNO-course-1340.git
```

Заходим в проект
```sh
cd 307818-EugeneINNO-course-1340
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
Пропишите в командной строке следующий код для создания .env файла переменных окружения и копирования туда стандартных переменных:
```sh
copy .env.template .env # Windows
cp .env.template .env # Linux / macOS
```
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
python3 .\lyceum\manage.py runserver
```
Сервер будет доступен по адресу: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

