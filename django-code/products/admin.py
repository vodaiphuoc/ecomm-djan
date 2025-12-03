from django.contrib import admin

from products.models import Category, Product, ProductImg

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug','parent')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price','stock','brand_name')
    search_fields = ('name', 'category','price')
    list_filter = ('category', 'price','stock')

@admin.register(ProductImg)
class ProductImgAdmin(admin.ModelAdmin):
    pass
