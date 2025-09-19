# articles/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SearchForm  # ← импортируем форму

# Статические данные — имитация базы статей
ARTICLES = [
    {
        'id': 1,
        'title': 'Python',
        'content': 'Python — высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Python используется в веб-разработке, анализе данных, машинном обучении и многом другом.',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg'
    },
    {
        'id': 2,
        'title': 'Django',
        'content': 'Django — это высокоуровневый веб-фреймворк на Python, который позволяет быстро создавать безопасные и масштабируемые веб-сайты. Он следует принципу DRY (Don’t Repeat Yourself).',
        'image': 'https://static.djangoproject.com/img/logos/django-logo-negative.png'
    },
    {
        'id': 3,
        'title': 'HTML',
        'content': 'HTML — стандартный язык разметки документов для просмотра веб-страниц в браузере. Является основой фронтенда. HTML описывает структуру веб-страницы с помощью тегов.',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/6/61/HTML5_logo_and_wordmark.svg'
    },
]

def home(request):
    theme = request.COOKIES.get('theme', 'light')
    last_query = request.COOKIES.get('last_search', '')

    # Создаём форму, передаём GET-данные, если есть
    form = SearchForm(request.GET or None)
    articles = ARTICLES  # По умолчанию — все статьи
    query = ''

    if form.is_valid():
        query = form.cleaned_data.get('q', '').strip()
        if query:
            articles = filter_articles(query)
            # Сохраняем в cookies только при успешном поиске
            response = render(request, 'articles/home.html', {
                'articles': articles,
                'theme': theme,
                'query': query,
                'last_query': query,
                'form': form,
            })
            response.set_cookie('last_search', query, max_age=30*24*60*60)
            return response

    # Если форма не валидна или GET пуст — показываем всё как есть
    context = {
        'articles': articles,
        'theme': theme,
        'query': query,
        'last_query': last_query,
        'form': form,
    }
    response = render(request, 'articles/home.html', context)
    return response

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

def filter_articles(query):
    """Фильтрует статьи по ключевому слову в заголовке или содержании"""
    if not query:
        return ARTICLES
    query_lower = query.lower()
    return [
        article for article in ARTICLES
        if query_lower in article['title'].lower() or query_lower in article['content'].lower()
    ]