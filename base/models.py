from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # add additional fields in here
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class PointCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    point = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PointTransaction(models.Model):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'is_student': True}
    )
    category = models.ForeignKey(PointCategory, on_delete=models.CASCADE)
    # points = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.category}"
