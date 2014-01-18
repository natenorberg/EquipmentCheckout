from django.contrib.auth.models import Group

# Create default checkout permission groups
if not Group.objects.filter(name="Music Education"):
    Group.objects.create(name="Music Education")
if not Group.objects.filter(name="Pre-Music Tech"):
    Group.objects.create(name="Pre-Music Tech")
if not Group.objects.filter(name="Music Tech"):
    Group.objects.create(name="Music Tech")
if not Group.objects.filter(name="Staff"):
    Group.objects.create(name="Staff")

# Create default site permission groups
if not Group.objects.filter(name="Monitor"):
    Group.objects.create(name="Monitor")