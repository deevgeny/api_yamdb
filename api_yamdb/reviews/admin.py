from django.contrib import admin

from reviews.models import Categories, Genres, Title


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)  # какие поля отображаются
    list_filter = ('name',)  # какие поля отображаются справа
    search_fields = ('name__startswith',)  # поиск
    list_display_links = ('name',)  # на какое поле можно кликнуть и зайти
    prepopulated_fields = {'slug': ('name',)}  # формирование слага из имени


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_filter = ('name',)
    search_fields = ('name__startswith',)
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description',)
    list_filter = ('genre', 'category',)
    search_fields = ('name__startswith', 'year',
                     'genre__startswith', 'category__startswith',)
    list_display_links = ('name', 'year',)
    empty_value_display = '-пусто-'  # заместо NULL
