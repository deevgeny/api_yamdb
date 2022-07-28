from django.contrib import admin

from reviews.models import Category, Genre, Title


@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)  # какие поля отображаются
    list_filter = ('name',)  # какие поля отображаются справа
    search_fields = ('name',)  # поиск
    list_display_links = ('name',)  # на какое поле можно кликнуть и зайти
    prepopulated_fields = {'slug': ('name',)}  # формирование слага из имени


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_filter = ('name',)
    search_fields = ('name',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description',)
    list_filter = ('genre', 'category', 'year',)
    search_fields = ('name', 'year', 'genre', 'category',)
    list_display_links = ('name', 'year',)
    empty_value_display = '-пусто-'  # заместо NULL
