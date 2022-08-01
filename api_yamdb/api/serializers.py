from datetime import date

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class ConfinedUserSerializer(serializers.ModelSerializer):
    """Сериализатор ????."""

    class Meta:
        model = User
        fields = ("username", "email")


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор кастомной модели пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class CategoriesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели категория."""

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Category.objects.all(),
                fields=["name", "slug"],
                message="This record has already been created!",
            )
        ]


class GenresSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанров."""

    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Genre.objects.all(),
                fields=["name", "slug"],
                message="This record has already been created!",
            )
        ]


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для модели произведения, для чтения данных."""

    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    description = serializers.CharField(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=["name", "year"],
                message="This record has already been created!",
            )
        ]

        def validate_year(self, value):
            current_year = date.today().year
            if not (value <= current_year):
                raise serializers.ValidationError(
                    "Нельзя добавлять произведения, которые еще не вышли."
                    "Год выпуска не может быть больше текущего года."
                )
            return value

    def get_rating(self, obj):
        """Calculate title rating."""
        # Посмотреть, может сделать лучше
        if obj.reviews.count() > 0:
            return obj.reviews.aggregate(rating=Avg("score"))["rating"]


class TitleCreateSerializer(TitleReadSerializer):
    """Сериализатор для модели произведения, для записи данных."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field="slug", many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field="slug",
    )


class ReviewSerializer(serializers.ModelSerializer):
    """Review serializer."""

    text = serializers.CharField()
    score = serializers.IntegerField(max_value=10, min_value=1)
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("id", "title", "author", "pub_date")
        # здесь попробовать юник констрэнт


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("id", "author", "pub_date")
