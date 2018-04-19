"""WebTechnology_Course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/$', views.login),
    url(r'^register/$', views.register),
    url(r'^logout/$', views.logout),
    url(r'^contact/$', views.contact),
    url(r'^error/[a-zA-Z0-9]+$', views.error),
    url(r'^author/[0-9]+$', views.author),
    url(r'^author/$', views.author),
    url(r'^genre/[0-9]+$', views.genre),
    url(r'^genre/$', views.genre),
    url(r'^book/[0-9]+$', views.book),
    url(r'^book/[0-9]+/chapter/[0-9]+/read$', views.read),
    url(r'^book/add$', views.add_book),
    url(r'^book/[0-9]+/addchapter$', views.add_chapter),
    url(r'^book/[0-9]+/chapter/[0-9]+/edit$', views.edit_chapter),
    url(r'^book/[0-9]+/vote/[0-9]+$', views.vote)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)