from django.contrib import admin
from .models import *


admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(BookRating)
admin.site.register(BookChapter)
