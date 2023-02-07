from django.urls import path

from . import views




urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("random_entry/", views.random_entry, name="random_entry"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save")
]
