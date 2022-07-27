from rest_framework import serializers

from reviews.models import Categories, Genres, Title


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug',)
#        exclude = ('id', )  или fields = ('name', 'slug',)


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug',)
#        exclude = ('id', )  или fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        exclude = ('id',)
        #   read_only_fields = ('rating',) раскоментировать после слияние веток
