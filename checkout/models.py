from django.db import models


class Equipment(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField('date published')
    quantity = models.IntegerField(max_length=200)

    def __str__(self):
        return self.name