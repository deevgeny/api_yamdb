from datetime import date

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class RegisterUserSerializer(serializers.ModelSerializer):
    """User model serializer for user registration."""

    class Meta:
        model = User
        fields = ("username", "email")


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

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
    """Category model serializer."""

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
    """Genre model serializer."""

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


class TitleSerializer(serializers.ModelSerializer):
    """Title model serializer."""

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
                    "Title year should be less or equal to current year!"
                )
            return value

    def get_rating(self, obj):
        """Calculate title rating."""
        if obj.reviews.count() > 0:
            return obj.reviews.aggregate(rating=Avg("score"))["rating"]


class CreateTitleSerializer(TitleSerializer):
    """Title model serializer for create operation."""

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


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer."""

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
        read_only_fields = ("id", "author", "pub_date")
