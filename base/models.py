from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


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
        related_name='receiving_point',
        on_delete=models.CASCADE,
        limit_choices_to={'is_student': True}
    )
    teacher = models.ForeignKey(
        CustomUser,
        related_name='giving_point',
        on_delete=models.CASCADE,
        limit_choices_to={'is_teacher': True}
    )
    category = models.ForeignKey(PointCategory, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-category']

    def __str__(self):
        return f"{self.student} - {self.category}"


@receiver(pre_save, sender=PointTransaction)
def set_teacher(sender, instance, **kwargs):
    if not instance.teacher_id:
        current_user = get_user_model().objects.get(pk=instance.teacher_id)
        if (current_user and
                current_user.is_authenticated and
                current_user.is_teacher):
            instance.teacher = current_user
