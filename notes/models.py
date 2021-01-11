from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Group(models.Model):
    group_name = models.CharField(max_length=50, unique=True)

    def __save__(self, *args, **kwargs):
        self.group_name = self.group_name.lower()
        super(Group, self).save(*args, **kwargs)

    def __str__(self):
        return self.group_name.capitalize()

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='notes', related_name='notes')
    group = models.ForeignKey(Group, on_delete=models.SET_DEFAULT, default=1)
    create_date = models.DateTimeField()
    planned_date = models.DateTimeField()
    text = models.CharField(max_length=255)

    def __save__(self, *args, **kwargs):
        self.create_date = timezone.now()
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return 'User{0} note for {1}'.format(self.id, self.planned_date)
