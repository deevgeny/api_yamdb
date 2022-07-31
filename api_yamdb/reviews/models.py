from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
        help_text="Добавьте название категории",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Уникальный адрес категории",
        help_text="Добавьте адрес категории",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="exclude the re-creation of the сategory",
                fields=["name", "slug"],
            )
        ]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название жанра",
        help_text="Добавьте название жанра",
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Уникальный адрес жанра",
        help_text="Добавьте адрес жанра",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="exclude the re-creation of the genre",
                fields=["name", "slug"],
            )
        ]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения",
        help_text="Добавьте название произведения",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска произведения",
        help_text="Добавьте год выпуска произведения",
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="Описание произведения",
        help_text="Добавьте описание произведения",
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанр",
        help_text="Выберите жанр",
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Категория",
        help_text="Выберите категорию",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="exclude the re-creation of the titles",
                fields=["name", "year"],
            )
        ]
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class Review(models.Model):
    """Review model."""

    RATING_CHOICES = [
        (None, "---"),
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
        (6, "6"),
        (7, "7"),
        (8, "8"),
        (9, "9"),
        (10, "10"),
    ]

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="rating",
        verbose_name="Отзыв",
        help_text="Выберите произведение",
    )
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="review",
    )
    score = models.IntegerField(
        verbose_name="Оценка",
        help_text="Дайте оценку произведению от 1 до 10",
        choices=RATING_CHOICES,
        default="---",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.title_id


class Comment(models.Model):
    """Comment model."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Обзор",
    )
    text = models.TextField(
        verbose_name="Комментарий",
        blank=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="comment",
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Комментарий к отзыву"
        verbose_name_plural = "Комментарии к отзывам"

    def __str__(self):
        return self.review_id
