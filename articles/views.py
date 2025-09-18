# articles/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Статические данные — имитация базы статей
ARTICLES = [
    {
        'id': 1,
        'title': 'Python',
        'content': 'Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Первый релиз вышел в 1991 году, автор — Гвидо ван Россум.',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg'
    },
    {
        'id': 2,
        'title': 'Django',
        'content': 'Django — это высокоуровневый веб-фреймворк на Python, который позволяет быстро создавать безопасные и масштабируемые веб-сайты. Назван в честь джазового гитариста Джанго Рейнхардта.',
        'image': 'https://static.djangoproject.com/img/logos/django-logo-negative.png'
    },
    {
        'id': 3,
        'title': 'HTML',
        'content': 'HTML — стандартный язык разметки документов для просмотра веб-страниц в браузере. Является основой фронтенда. Первая версия появилась в 1993 году, разработчик — Тим Бернерс-Ли.',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/6/61/HTML5_logo_and_wordmark.svg'
    },
]

def home(request):
    # Получаем тему из cookies, по умолчанию — светлая
    theme = request.COOKIES.get('theme', 'light')
    context = {
        'articles': ARTICLES,
        'theme': theme,
    }
    return render(request, 'articles/home.html', context)


def article_detail(request, article_id):
    theme = request.COOKIES.get('theme', 'light')
    article = next((a for a in ARTICLES if a['id'] == article_id), None)
    if not article:
        return HttpResponse("Статья не найдена", status=404)
    context = {
        'article': article,
        'theme': theme,
    }
    return render(request, 'articles/article_detail.html', context)


def set_theme(request):
    # Получаем выбранную тему из GET-параметра
    theme = request.GET.get('theme', 'light')
    # Определяем, куда перенаправить (откуда пришёл пользователь)
    next_url = request.META.get('HTTP_REFERER', '/')
    # Создаём ответ с перенаправлением
    response = redirect(next_url)
    # Устанавливаем cookie на 30 дней
    response.set_cookie('theme', theme, max_age=30*24*60*60)
    return response