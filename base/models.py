from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """ customizing the user model """
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class PointCategory(models.Model):
    """ Category list for awarding points """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    point = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PointTransaction(models.Model):
    """ Class for awarding points to students """
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'is_student': True}
    )
    category = models.ForeignKey(PointCategory, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-category']

    def __str__(self):
        return f"{self.student} - {self.category}"
