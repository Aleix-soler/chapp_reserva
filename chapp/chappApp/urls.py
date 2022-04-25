from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path('book/form/1', firstForm),
    path('book/form/2', secondForm),
    path('book/form/3', thirdForm),
    path('book/delete/<id>', deleteBook),
    path('book/export/csv', export_books_excel),
    path('book/view/<id>', view_book),
    path('', book_list, name="Book List")
]