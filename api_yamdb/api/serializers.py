from rest_framework import serializers

from reviews.models import Category, Genre, Title
from users.models import User


class ConfinedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class UserSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Category
        fields = ('name', 'slug',)
#        exclude = ('id', )  или fields = ('name', 'slug',)


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)
#        exclude = ('id', )  или fields = ('name', 'slug',)


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(read_only=True, many=True)
    description = serializers.CharField(required=False)
    #    rating = рейтинг от Германа

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
#        fields = '__all__'.


class TitleCreateSerializer(TitleReadSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug', )
