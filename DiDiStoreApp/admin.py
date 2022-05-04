from django.contrib import admin
from .models import Profile,MainCategory,Category,Author,Publisher,Book,Order,OrderItem
# Register your models here.

class BookAdmin(admin.ModelAdmin):
    search_fields = ("name","publisher","author","price")
    list_filter = ("name","publisher","author","year")
    list_display = ("id","name","author","year","price")

admin.site.register(Profile)
admin.site.register(MainCategory)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book,BookAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)

