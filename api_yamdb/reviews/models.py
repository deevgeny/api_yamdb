from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
        help_text="Добавьте название категории"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Уникальный адрес категории",
        help_text="Добавьте адрес категории"
    )

    class Meta:
        # ordering = ('name',)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название жанра",
        help_text="Добавьте название жанра"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Уникальный адрес жанра",
        help_text="Добавьте адрес жанра"
    )

    class Meta:
        # ordering = ('name',)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения",
        help_text="Добавьте название произведения"
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска произведения",
        help_text="Добавьте год выпуска произведения"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание произведения",
        help_text="Добавьте описание произведения"
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name="Жанр",
        help_text='Выберите жанр'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name="Категория",
        help_text="Выберите категорию"
    )

    class Meta:
        # ordering = ('name',)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name
