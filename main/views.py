from django.http import HttpResponse
from django.shortcuts import render
from django.template import  loader


def index(request):
  return render(request, "index.html",)


def cart(request):
  return render(request, "cart.html",)


def contact(request):
  return render(request, "contact.html",)


def detail(request):
  return render(request, "detail.html",)