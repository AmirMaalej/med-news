from rest_framework import viewsets

from . import serializers
from . import models


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.none()

    def get_serializer_class(self):
        return serializers.AuthorSerializer

    def get_queryset(self):
        return models.Author.objects.all()

    def perform_create(self, serializer):
        serializer.save()