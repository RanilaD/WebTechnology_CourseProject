from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, BookChapter


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'type': 'email', 'placeholder': 'example@example.com'}))
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Имя"
        self.fields['contact_email'].label = ""
        self.fields['content'].label = "Сообщение"


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'type': 'email', 'placeholder': 'example@example.com'}))
    email.label = ""

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class AddBookForm(forms.Form):
    title = forms.CharField(required=True)
    author = forms.CharField(required=True)
    cover = forms.ImageField(required=False)
    isbn = forms.CharField(required=False)
    genre = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Название"
        self.fields['author'].label = "Автор (ФИ[О])"
        self.fields['description'].label = "Описание"
        self.fields['isbn'].label = "ISBN"
        self.fields['genre'].label = "Жанры"
        self.fields['cover'].label = ""


class AddChapterForm(forms.Form):
    title = forms.CharField(required=True)
    text = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(AddChapterForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Название"
        self.fields['text'].label = "Текст"
