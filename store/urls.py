from django.contrib import admin
from django.urls import path, include

from main import views

urlpatterns = [
    path('add-item-to-cart/<int:pk>', views.add_item_to_cart, name='add_item_to_cart'),
]
