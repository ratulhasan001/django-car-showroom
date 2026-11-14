from django.db import models
from django.utils.text import slugify


class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # The brand filter links use the slug, so make sure every brand has one
        # (the admin pre-fills it, but brands created elsewhere might not).
        if not self.slug:
            base = slugify(self.name)[:90] or 'brand'
            slug, n = base, 2
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
