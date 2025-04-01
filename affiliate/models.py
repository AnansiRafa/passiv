# affiliate/models.py
from django.db import models


class AffiliateLink(models.Model):
    url = models.URLField()
    description = models.CharField(max_length=255)
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return self.description
