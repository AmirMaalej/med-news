from rest_framework import serializers

from . import models


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Author
        fields = ('id', 'name', 'title', 'bio')