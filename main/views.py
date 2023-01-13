from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from store.models import Product


def index(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, "index.html", context=context)


def cart(request):
    return render(request, "cart.html", )


def contact(request):
    return render(request, "contact.html", )


def detail(request, pk):
    context = {
        "product": Product.objects.filter(id=pk).first()
    }

    return render(request, "detail.html", context=context)
