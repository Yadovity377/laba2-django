# 📚 Онлайн-энциклопедия — Docker + PostgreSQL (Django 5.2)

Проект реализует веб-приложение для управления статьями и книгами: поиск, добавление, экспорт в JSON, переключение темы (светлая/тёмная), адаптивный интерфейс.  
Соответствует промышленным стандартам: отказоустойчивость (PostgreSQL), изоляция (Docker), безопасность (env), сборка (multi-stage).  
Требование лабораторной: приложение, работающее на PythonAnywhere, теперь упаковано в Docker-контейнеры и переведено с SQLite на PostgreSQL.

🔗 **Демо**: [https://yadovity.pythonanywhere.com](https://yadovity.pythonanywhere.com)

> ⚠️ Согласно [Django Deployment Docs](https://docs.djangoproject.com/en/5.2/howto/deployment/):  
> *«The `runserver` command starts a lightweight development server, which is **not suitable for production**. Django currently supports two interfaces: WSGI and ASGI. WSGI is the main Python standard…»*

---

## 📦 Требования

| Компонент | Версия |
|----------|--------|
| **Docker Engine** | ≥ 24.0 |
| **Docker Compose** | ≥ 2.20 (v2, без `version:` в `docker-compose.yml`) |
| **Python** | 3.11+ (в контейнере — 3.13) |
| **WSL2** | Обязательно на Windows |

---

## 🧪 1. Запуск в режиме разработки

Используется **SQLite (по умолчанию)**, `runserver`, live-reload, volume-биндинги.

### 🔧 Шаги:

```bash
# 1. Клонирование
git clone https://github.com/Yadovity377/laba2-django.git
cd laba2-django

# 2. Настройка окружения
cp .env.example .env
# → замените SECRET_KEY на результат: 
# python -c "import secrets; print(secrets.token_urlsafe(50))"

# 3. Сборка и запуск
docker-compose up --build