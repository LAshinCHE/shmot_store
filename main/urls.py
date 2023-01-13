from django.contrib import admin
from django.urls import path, include

from main import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('detail/', views.detail, name='detail'),
    path('auth/', include('authentication.urls')),
]
