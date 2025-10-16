# articles/models.py

from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.CharField(max_length=100, verbose_name="Автор")
    year = models.IntegerField(verbose_name="Год издания")
    genre = models.CharField(max_length=50, verbose_name="Жанр")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        unique_together = ('title', 'author', 'year')