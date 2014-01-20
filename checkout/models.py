from datetime import datetime
from django.contrib.auth.models import User
from django.db import models


@property
def is_monitor(user):
    return user.groups.filter(name="monitor")


class Equipment(models.Model):
    name = models.CharField(max_length=500)
    brand = models.CharField(max_length=50, null=True, blank=True)
    date_added = models.DateTimeField('date published', auto_now_add=True)
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


class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='reserved_by')
    project = models.CharField(max_length=50)
    equipment = models.ManyToManyField('Equipment')
    reserved_time = models.DateTimeField(auto_now_add=True)  # Time reservation was placed by the student
    out_time = models.DateTimeField()  # Time reservation officially starts
    in_time = models.DateTimeField()  # Time equipment is due
    checked_out_time = models.DateTimeField(null=True, blank=True)  # Time equipment is actually checked out
    checked_in_time = models.DateTimeField(null=True, blank=True)  # Time equipment is actually returned
    is_approved = models.BooleanField()
    check_out_comments = models.TextField(null=True, blank=True)
    check_in_comments = models.TextField(null=True, blank=True)
    checked_out_by = models.ForeignKey(User, related_name='checked_out_by', null=True, blank=True)
    checked_in_by = models.ForeignKey(User, related_name='checked_in_by', null=True, blank=True)

    class Meta:
        ordering = ["out_time"]

    @property
    def is_ready(self):
        now = datetime.now()
        if self.checked_out_time is None and self.out_time >= now:
            return True
        else:
            return False

    @property
    def is_checked_out(self):
        if self.checked_out_time is not None and self.checked_in_time is None:
            return True
        else:
            return False

    @property
    def is_returned(self):
        if self.checked_out_time is not None and self.checked_in_time is not None:
            return True
        else:
            return False

    @property
    def is_overdue(self):
        if self.checked_out_time is not None and self.checked_in_time is None and self.in_time < datetime.now():
            return True
        else:
            return False

    @property
    def is_returned_late(self):
        if self.checked_in_time is not None and self.checked_in_time > self.in_time:
            return True
        else:
            return False