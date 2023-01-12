from django.contrib import admin

from store.models import Product,Payment,Order,OrderItem

admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
