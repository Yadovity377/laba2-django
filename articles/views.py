# articles/views.py

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.db import IntegrityError, models
import os
import json
import uuid
from .forms import SearchForm, BookForm, UploadBookForm
from .models import Book

# Статические данные — имитация базы статей
ARTICLES = [
    {
        'id': 1,
        'title': 'Python',
        'content': 'Python — высокоуровневый язык программирования общего назначения...',
        'image': 'image/python.webp'
    },
    {
        'id': 2,
        'title': 'Django',
        'content': 'Django — это высокоуровневый веб-фреймворк на Python...',
        'image': 'image/django.jpg'
    },
    {
        'id': 3,
        'title': 'HTML',
        'content': 'HTML — стандартный язык разметки документов...',
        'image': 'image/html.webp'
    },
]

BOOKS_DIR = os.path.join(settings.BASE_DIR, 'books')
os.makedirs(BOOKS_DIR, exist_ok=True)

def home(request):
    theme = request.GET.get('theme')
    if theme not in ['light', 'dark']:
        theme = request.COOKIES.get('theme', 'light')
    query = request.GET.get('q', '').strip()
    last_query = request.COOKIES.get('last_search', '')
    if query:
        articles = filter_articles(query)
        context = {'articles': articles, 'theme': theme, 'query': query, 'last_query': query, 'form': SearchForm({'q': query})}
        response = render(request, 'articles/home.html', context)
        response.set_cookie('last_search', query, max_age=30*24*60*60)
        response.set_cookie('theme', theme, max_age=30*24*60*60)
        return response
    context = {'articles': ARTICLES, 'theme': theme, 'query': '', 'last_query': last_query, 'form': SearchForm()}
    response = render(request, 'articles/home.html', context)
    response.set_cookie('theme', theme, max_age=30*24*60*60)
    return response

def article_detail(request, article_id):
    theme = request.GET.get('theme')
    if theme not in ['light', 'dark']:
        theme = request.COOKIES.get('theme', 'light')
    article = next((a for a in ARTICLES if a['id'] == article_id), None)
    if not article:
        return HttpResponse("Статья не найдена", status=404)
    context = {'article': article, 'theme': theme}
    response = render(request, 'articles/article_detail.html', context)
    if request.GET.get('theme') in ['light', 'dark']:
        response.set_cookie('theme', request.GET.get('theme'), max_age=30*24*60*60)
    return response

def filter_articles(query):
    if not query:
        return ARTICLES
    query_lower = query.lower()
    return [a for a in ARTICLES if query_lower in a['title'].lower() or query_lower in a['content'].lower()]

# === КНИГИ ===

def add_book(request):
    theme = request.GET.get('theme', request.COOKIES.get('theme', 'light'))
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            save_to = data.pop('save_to')
            if save_to == 'db':
                # Проверяем дубликат по уникальному набору полей
                if Book.objects.filter(
                    title=data['title'],
                    author=data['author'],
                    year=data['year']
                ).exists():
                    messages.warning(request, "Такая книга уже существует в базе данных.")
                else:
                    Book.objects.create(**data)
                    messages.success(request, "Книга успешно сохранена в базу данных!")
            else:
                filename = f"book_{uuid.uuid4().hex}.json"
                filepath = os.path.join(BOOKS_DIR, filename)
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                messages.success(request, "Книга успешно сохранена в JSON-файл!")
            return redirect('books_list')
    else:
        form = BookForm()
    response = render(request, 'articles/books_form.html', {'form': form, 'theme': theme})
    response.set_cookie('theme', theme, max_age=30*24*60*60)
    return response

def upload_book(request):
    theme = request.GET.get('theme', request.COOKIES.get('theme', 'light'))
    if request.method == 'POST':
        form = UploadBookForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            filename = f"book_{uuid.uuid4().hex}.json"
            filepath = os.path.join(BOOKS_DIR, filename)
            with open(filepath, 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            messages.success(request, "Файл успешно загружен и проверен!")
            return redirect('books_list')
    else:
        form = UploadBookForm()
    response = render(request, 'articles/books_upload.html', {'form': form, 'theme': theme})
    response.set_cookie('theme', theme, max_age=30*24*60*60)
    return response

def books_list(request):
    theme = request.GET.get('theme', request.COOKIES.get('theme', 'light'))
    source = request.GET.get('source', 'file')
    books = []
    if source == 'db':
        books = Book.objects.all()
    else:
        if os.path.exists(BOOKS_DIR):
            for filename in os.listdir(BOOKS_DIR):
                if filename.endswith('.json'):
                    filepath = os.path.join(BOOKS_DIR, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            required = {'title', 'author', 'year', 'genre'}
                            if isinstance(data, dict) and required.issubset(data.keys()):
                                data['filename'] = filename
                                books.append(data)
                    except Exception:
                        continue
    response = render(request, 'articles/books_list.html', {
        'books': books,
        'theme': theme,
        'source': source
    })
    response.set_cookie('theme', theme, max_age=30*24*60*60)
    return response

def delete_book(request):
    if request.method == 'POST':
        filename = request.POST.get('filename')
        filepath = os.path.join(BOOKS_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            messages.success(request, "Книга успешно удалена!")
    return HttpResponseRedirect(reverse('books_list'))

def delete_book_db(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    messages.success(request, "Книга удалена из базы данных!")
    return redirect('books_list')

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    theme = request.COOKIES.get('theme', 'light')
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data.pop('save_to', None)

            # Проверка на дубликат (исключая текущую запись)
            if Book.objects.filter(
                title=data['title'],
                author=data['author'],
                year=data['year']
            ).exclude(pk=pk).exists():
                messages.warning(request, "Книга с такими данными уже существует в базе.")
                return render(request, 'articles/books_form.html', {'form': form, 'theme': theme})

            for key, value in data.items():
                setattr(book, key, value)
            book.save()
            messages.success(request, "Книга обновлена!")
            return redirect('books_list')
    else:
        form = BookForm(initial={
            'title': book.title,
            'author': book.author,
            'year': book.year,
            'genre': book.genre,
            'save_to': 'db'
        })
    return render(request, 'articles/books_form.html', {'form': form, 'theme': theme})

def book_search(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(author__icontains=query) |
            models.Q(genre__icontains=query)
        )
        results = [{'id': b.id, 'title': b.title, 'author': b.author, 'year': b.year, 'genre': b.genre} for b in books]
        return JsonResponse(results, safe=False)
    return JsonResponse([], safe=False)