from django.db import models
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    name = models.CharField(_('Name'), max_length=50)
    title = models.CharField(_('Title'), max_length=50)
    bio = models.TextField(_('Bio'), max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'author'
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
