# articles/forms.py

from django import forms
import json

class SearchForm(forms.Form):
    q = forms.CharField(
        label='',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по энциклопедии...',
            'class': 'form-control'
        })
    )

class BookForm(forms.Form):
    title = forms.CharField(max_length=200, label="Название книги", widget=forms.TextInput(attrs={'class': 'form-control'}))
    author = forms.CharField(max_length=100, label="Автор", widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.IntegerField(min_value=1000, max_value=2025, label="Год издания", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    genre = forms.CharField(max_length=50, label="Жанр", widget=forms.TextInput(attrs={'class': 'form-control'}))
    save_to = forms.ChoiceField(
        choices=[('file', 'Сохранить в JSON-файл'), ('db', 'Сохранить в базу данных')],
        widget=forms.RadioSelect,
        label="Способ сохранения"
    )

class UploadBookForm(forms.Form):
    file = forms.FileField(label="Загрузите JSON-файл с книгой")

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith('.json'):
            raise forms.ValidationError("Разрешены только файлы с расширением .json")
        try:
            data = json.load(file)
            required_keys = {'title', 'author', 'year', 'genre'}
            if not isinstance(data, dict) or not required_keys.issubset(data.keys()):
                raise forms.ValidationError("Файл не содержит корректную структуру книги")
            if not (isinstance(data['year'], int) and 1000 <= data['year'] <= 2025):
                raise forms.ValidationError("Год должен быть целым числом от 1000 до 2025")
        except (ValueError, json.JSONDecodeError):
            raise forms.ValidationError("Файл не является валидным JSON")
        file.seek(0)
        return file