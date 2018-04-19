from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=128, help_text="Введите название жанра")

    def get_absolute_url(self):
        return f"/genre/{self.id}"

    def __str__(self):
        return self.name

    @property
    def get_first_letter(self):
        return self.name[0].upper()


class Language(models.Model):
    name = models.CharField(max_length=128, help_text="Введите язык")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    surname = models.CharField(max_length=128, null=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name} {self.surname or ''}"

    def get_absolute_url(self):
        return f"/author/{self.id}"

    @property
    def get_first_letter(self):
        return self.last_name[0].upper()


class BookRating(models.Model):
    user = models.ForeignKey(User)
    rating = models.IntegerField()
    book = models.ForeignKey('Book')

    def __str__(self):
        return f"{self.user.username} {self.book.title} - {self.rating}"


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=2048)
    isbn = models.CharField('ISBN', max_length=13)
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey(Language)
    cover = models.ImageField(upload_to="media")
    upload_date = models.DateField(auto_now=True)
    uploaded_by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @property
    def get_rating(self):
        ratings = BookRating.objects.all().filter(book=self)
        if ratings:
            a = 0
            for r in ratings:
                a += r.rating
            a /= ratings.__len__()
            return "%.2f" % (a)
        else:
            return "Нет оценок"

    @property
    def get_genres(self):
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    @property
    def get_absolute_url(self):
        return f"/book/{self.id}"

    def __str__(self):
        return self.title


class BookChapter(models.Model):
    title = models.CharField(max_length=128, help_text="Введите название главы")
    chapter_number = models.IntegerField()
    upload_date = models.DateField(auto_now=True)
    raw_html_text = models.CharField(max_length=262140)
    book = models.ForeignKey(Book)
    prev_chapter = models.ForeignKey("BookChapter", related_name="prevchapter", blank=True, null=True)
    next_chapter = models.ForeignKey("BookChapter", related_name="nextchapter", blank=True, null=True)

    @property
    def get_absolute_url(self):
        return f"/book/{self.book.id}/chapter/{self.id}/read"

    @property
    def get_edit_url(self):
        return f"/book/{self.book.id}/chapter/{self.id}/edit"

    @property
    def get_delete_url(self):
        return f"/book/{self.book.id}/chapter/{self.id}/delete"

    def __str__(self):
        return self.title