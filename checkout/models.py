from django.db import models


class Equipment(models.Model):
    name = models.CharField(max_length=200)
    date_added = models.DateTimeField('date published')
    quantity = models.IntegerField(max_length=200)
    condition = models.CharField(max_length=200)
    description = models.TextField()
    #Permissions
    music_ed = models.BooleanField('Music Education', default=False)
    pre_gate = models.BooleanField('Pre-Music Tech', default=False)
    post_gate = models.BooleanField('Music Tech', default=True)
    staff = models.BooleanField(default=True)

    def __str__(self):
        return self.name