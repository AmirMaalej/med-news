from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.author.models import Author


class Article(models.Model):
    title = models.CharField(_('Title'), max_length=50)
    body = models.TextField(_('Body'), max_length=500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')