# articles/views.py

from django.shortcuts import render, HttpResponse
from .forms import SearchForm

# Статические данные — имитация базы статей
ARTICLES = [
    {
        'id': 1,
        'title': 'Python',
        'content': 'Python — высокоуровневый язык программирования общего назначения...',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg'
    },
    {
        'id': 2,
        'title': 'Django',
        'content': 'Django — это высокоуровневый веб-фреймворк на Python...',
        'image': 'https://static.djangoproject.com/img/logos/django-logo-negative.png'
    },
    {
        'id': 3,
        'title': 'HTML',
        'content': 'HTML — стандартный язык разметки документов...',
        'image': 'https://upload.wikimedia.org/wikipedia/commons/6/61/HTML5_logo_and_wordmark.svg'
    },
]

def home(request):
    # 1. Сначала проверяем, пришёл ли запрос на смену темы
    theme = request.GET.get('theme')
    if theme in ['light', 'dark']:
        # Если да — устанавливаем новую тему в cookies
        response = _render_home_page(request, theme)
        response.set_cookie('theme', theme, max_age=30*24*60*60)
        return response

    # 2. Если нет — берём тему из cookies
    theme = request.COOKIES.get('theme', 'light')

    # 3. Обрабатываем поиск
    query = request.GET.get('q', '').strip()
    last_query = request.COOKIES.get('last_search', '')

    if query:
        articles = filter_articles(query)
        context = {
            'articles': articles,
            'theme': theme,
            'query': query,
            'last_query': query,
            'form': SearchForm({'q': query}),
        }
        response = render(request, 'articles/home.html', context)
        response.set_cookie('last_search', query, max_age=30*24*60*60)
        return response

    # 4. Показываем главную страницу
    context = {
        'articles': ARTICLES,
        'theme': theme,
        'query': '',
        'last_query': last_query,
        'form': SearchForm(),
    }
    response = render(request, 'articles/home.html', context)
    return response

def _render_home_page(request, theme):
    """Вспомогательная функция для рендеринга главной страницы"""
    query = request.GET.get('q', '').strip()
    last_query = request.COOKIES.get('last_search', '')

    if query:
        articles = filter_articles(query)
        context = {
            'articles': articles,
            'theme': theme,
            'query': query,
            'last_query': query,
            'form': SearchForm({'q': query}),
        }
        return render(request, 'articles/home.html', context)

    context = {
        'articles': ARTICLES,
        'theme': theme,
        'query': '',
        'last_query': last_query,
        'form': SearchForm(),
    }
    return render(request, 'articles/home.html', context)

def article_detail(request, article_id):
    # Получаем тему из GET-параметра (если есть)
    theme = request.GET.get('theme')
    if theme not in ['light', 'dark']:
        theme = request.COOKIES.get('theme', 'light')

    article = next((a for a in ARTICLES if a['id'] == article_id), None)
    if not article:
        return HttpResponse("Статья не найдена", status=404)
    context = {
        'article': article,
        'theme': theme,
    }
    response = render(request, 'articles/article_detail.html', context)
    if request.GET.get('theme') in ['light', 'dark']:
        response.set_cookie('theme', request.GET.get('theme'), max_age=30*24*60*60)
    return response

def filter_articles(query):
    """Фильтрует статьи по ключевому слову в заголовке или содержании"""
    if not query:
        return ARTICLES
    query_lower = query.lower()
    return [
        article for article in ARTICLES
        if query_lower in article['title'].lower() or query_lower in article['content'].lower()
    ]