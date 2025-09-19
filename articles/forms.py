# articles/forms.py

from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(
        label='Поиск',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Поиск по статьям...',
            'class': 'search-input'
        })
    )