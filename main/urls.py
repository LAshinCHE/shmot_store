from django.contrib import admin
from django.urls import path, include

from main import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('admin/', admin.site.urls),
]
