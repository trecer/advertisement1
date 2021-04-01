from django.contrib import admin
from .models import News, Category



class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published',)
    list_display_links = ('id', 'title') # делает поля ссылками
    search_fields = ('title', 'content') # определяет по каким параметрам поиск
    list_editable = ('is_published',) # редактирование не входя в статью конкретного поля
    list_filter = ('is_published', 'category',) # По каким полям фильтруем


admin.site.register(News, NewsAdmin) # Добавляет модель в админку


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

admin.site.register(Category, CategoryAdmin)