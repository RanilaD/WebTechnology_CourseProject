from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth import login as log_in, authenticate, logout as log_out
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from WebTechnology_Course.forms import *
from django.core.mail import send_mail
from .models import *


def index(request):
    context = {}
    books = Book.objects.all().order_by('?')[:3]
    books1 = Book.objects.all().order_by('-upload_date')[:3]
    context['new_books'] = books1
    context['books'] = books
    return render(request, 'index.html', context, RequestContext(request))


def error(request):
    context = {}
    return render(request, 'error.html', context, RequestContext(request))


@csrf_exempt
def contact(request):
    form = ContactForm
    context = {
        "form": form
    }
    if request.method == "POST":
        name = request.POST['contact_name']
        msg = request.POST['content']
        email = request.POST['contact_email']
        send_mail(f'Обратная связь: {name}', msg, email, ['localhost@mail.com'])
        return HttpResponseRedirect("/")
    else:
        return render(request, 'contact.html', context, RequestContext(request))


@csrf_exempt
def login(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['login_username'], password=request.POST['login_password'])
        if user is not None:
            log_in(request, user)
            ret_url = request.POST['login_return_url']
            if ret_url == "/login/" or ret_url == "/register/":
                ret_url = "/"
            return HttpResponseRedirect(ret_url)
        else:
            return render(request, 'error.html', {'error_text': "Неверный логин или пароль"}, RequestContext(request))
    else:
        return HttpResponseRedirect("/")


@csrf_exempt
def register(request):
    if request.method == "POST":
        new_user = UserCreationForm(request.POST)
        if new_user.is_valid():
            new_user.save()
            user = authenticate(request, username=new_user.cleaned_data['username'], password=new_user.cleaned_data['password2'])
            log_in(request, user)
            ret_url = request.POST['registration_return_url']
            if ret_url == "/login/" or ret_url == "/register/":
                ret_url = "/"
            return HttpResponseRedirect(ret_url)
        else:
            return render(request, 'error.html', {'form': new_user}, RequestContext(request))
    else:
        return HttpResponseRedirect("/")


def logout(request):
    if request.user.is_authenticated():
        log_out(request)
    return HttpResponseRedirect('/')


@csrf_exempt
def add_book(request):
    form = AddBookForm(request.POST, request.FILES)
    context = {
        "form": form,
        "error": ""
    }
    if request.method == "GET":
        return render(request, 'add_book.html', context, RequestContext(request))
    else:
        book = Book()
        # ищем автора в базе
        author = Author()
        author_name = request.POST['author'].split()
        genres = request.POST['genre'].split()
        title = request.POST['title']
        isbn = request.POST['isbn']
        cover = None #request.POST['cover']
        description = request.POST['description']

        # Ищем автора или добавляем нового
        if author_name.__len__() < 2 or author_name.__len__() > 3:
            context['error'] += "<li>Неверно задано имя автора</li>"
        else:
            if author_name.__len__() == 2:
                author.last_name = author_name[0]
                author.first_name = author_name[1]
                author.surname = ""
            else:
                author.last_name = author_name[0]
                author.first_name = author_name[1]
                author.surname = author_name[2]
        a = Author.objects.get_or_create(first_name=author.first_name, last_name=author.last_name, surname=author.surname)
        book.author = Author.objects.all().filter(first_name=author.first_name, last_name=author.last_name, surname=author.surname).first()
        book.title = title
        book.id = Book.objects.all().last().id + 1
        book.language = Language.objects.all().first()
        book.isbn = isbn or "000000000000"
        from datetime import date
        book.upload_date = date.today()
        book.uploaded_by_user = request.user
        book.cover = cover
        book.description = description
        book.language = Language.objects.all().first()
        _genres = ()
        for genre in genres:
            g = Genre.objects.get_or_create(name=genre)
            _genres.__add__(g)
        if _genres:
            book.genre.add(*_genres)
        if context['error'].__len__() > 0:
            return render(request, 'add_book.html', context, RequestContext(request))
        else:
            cover = request.FILES['cover']
            from django.core.files.storage import FileSystemStorage
            import uuid
            fs = FileSystemStorage()
            filename = f"cover_{uuid.uuid4().hex[:7:]}.jpg"
            fname = fs.save(name=filename, content=cover)
            book.cover = fname
            book.save()
            return HttpResponseRedirect(book.get_absolute_url)


@csrf_exempt
def add_chapter(request):
    form = AddChapterForm(request.POST)
    context = {
        "form": form,
        "error": "",
        "actoin_url": ""
    }
    t = request.path.split('/')
    book = Book.objects.all().filter(id=int(t[t.__len__() - 2])).first()
    all_chapters = BookChapter.objects.filter(book=book)
    prev_chapter = all_chapters.all().last()
    context['action_url'] = f"{book.get_absolute_url}/addchapter"
    if request.method == "GET":
        return render(request, 'add_chapter.html', context, RequestContext(request))
    else:
        chapter = BookChapter()
        text = request.POST['text']
        title = request.POST['title']

        chapter.title = title
        chapter.id = BookChapter.objects.all().last().id + 1 or 1
        if prev_chapter:
            chapter.chapter_number = prev_chapter.chapter_number + 1
            chapter.prev_chapter = prev_chapter
        else:
            chapter.chapter_number = 1
        chapter.book = book
        raw_html_text = ""
        for line in text.split('\n'):
            raw_html_text += f"<p>{line}</p>"
        chapter.raw_html_text = raw_html_text
        chapter.save()
        chapters = BookChapter.objects.filter(book=book)
        if chapters.__len__() > 1:
            prev_chapter.next_chapter = chapters.last()
            prev_chapter.save()
        return HttpResponseRedirect(book.get_absolute_url)


@csrf_exempt
def edit_chapter(request):
    context = {
        "error": "",
        "actoin_url": ""
    }
    t = request.path.split('/')
    chapter = BookChapter.objects.all().filter(id=t[t.__len__() - 2]).first()
    context['text'] = chapter.raw_html_text.replace("<p>", "").replace("</p>", "\n")
    context['title'] = chapter.title
    context['action_url'] = chapter.get_edit_url

    if request.method == "GET":
        return render(request, 'edit_chapter.html', context, RequestContext(request))
    else:
        text = request.POST['text']
        raw_html_text = ""
        for line in text.split('\n'):
            raw_html_text += f"<p>{line}</p>"
        chapter.raw_html_text = raw_html_text
        chapter.title = request.POST['title']
        chapter.save()
        return HttpResponseRedirect(chapter.get_absolute_url)


def author(request):
    context = {}
    t = request.path.split('/')
    if t[t.__len__() - 1] == '':
        context['authors'] = Author.objects.all().order_by('last_name', 'first_name')
        return render(request, 'author_all.html', context, RequestContext(request))
    _author = Author.objects.all().filter(id=int(t[t.__len__() - 1])).first()
    books = Book.objects.all().filter(author=_author).order_by('title')
    if author:
        context["author"] = _author
        context["books"] = books
    else:
        context['error_text'] = f"Автор с id = {t[t.__len__() - 1]} не существует"
        return render(request, 'error.html', context, RequestContext(request))
    return render(request, 'author.html', context, RequestContext(request))


def genre(request):
    context = {}
    t = request.path.split('/')
    if t[t.__len__() - 1] == '':
        context['genres'] = Genre.objects.all().order_by('name')
        return render(request, 'genre_all.html', context, RequestContext(request))
    _genre = Genre.objects.all().filter(id=int(t[t.__len__() - 1])).first()
    books = Book.objects.all().filter(genre=_genre).order_by('title')
    if _genre:
        context["genre"] = _genre
        if books:
            context["books"] = books
        else:
            context["books_not_found"] = f"""Книг жанра "{_genre}" не найдено"""
    else:
        context['error_text'] = f"Жанр с id = {t[t.__len__() - 1]} не существует"
        return render(request, 'error.html', context, RequestContext(request))
    return render(request, 'genre.html', context, RequestContext(request))


def book(request):
    context = {
        "user_has_voted": True
    }
    t = request.path.split('/')
    _book = Book.objects.all().filter(id=int(t[t.__len__() - 1])).first()
    chapters = BookChapter.objects.all().filter(book=_book).order_by('chapter_number')
    if _book:
        if request.user.is_authenticated:
            v = BookRating.objects.all().filter(book=_book, user=request.user).first()
            context['user_has_voted'] = v

        context["book"] = _book
        if chapters:
            context["chapters"] = chapters
        else:
            context["chapters_null"] = f"""В данной книге пока еще нет глав"""
    else:
        context['error_text'] = f"Книги с id = {t[t.__len__() - 1]} не существует"
        return render(request, 'error.html', context, RequestContext(request))
    return render(request, 'book.html', context, RequestContext(request))


def vote(request):
    t = request.path.split('/')
    book = Book.objects.all().filter(id=int(t[t.__len__() - 3])).first()
    user = request.user
    rating = BookRating()
    rating.book = book
    rating.user = user
    rating.rating = int(t[t.__len__() - 1])
    rating.save()
    return HttpResponseRedirect(book.get_absolute_url)


def read(request):
    context = {}
    t = request.path.split('/')
    context["temp"] = t
    chapter = BookChapter.objects.all().filter(id=int(t[t.__len__() - 2])).first()
    _book = Book.objects.all().filter(id=int(t[t.__len__() - 4])).first()
    if chapter:
        if book:
            context["book"] = _book
        context["chapter"] = chapter
        context["raw_html"] = chapter.raw_html_text
    else:
        context["error_text"] = f"Главы с id = {t[t.__len__() - 2]} не существует"
        return render(request, 'error.html', context, RequestContext(request))
    return render(request, 'reader/reader.html', context, RequestContext(request))