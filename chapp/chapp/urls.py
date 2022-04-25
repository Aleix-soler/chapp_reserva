from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
import chappApp.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(chappApp.urls))
]
