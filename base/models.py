from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    """ customizing the user model """
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    grade = models.CharField(max_length=10, null=True, blank=True)
    adm_no = models.PositiveIntegerField(null=True, blank=True, unique=True)
    parent_contact = models.CharField(max_length=15, null=True, blank=True)


class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    designation = models.CharField(max_length=30, null=True, blank=True)
    reg_no = models.PositiveIntegerField(null=True, blank=True, unique=True)
    contact = models.CharField(max_length=15, null=True, blank=True)


@receiver(post_save, sender=CustomUser)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.is_student:
        StudentProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_student_profile(sender, instance, **kwargs):
    if instance.is_student:
        student_profile, created = StudentProfile.objects.get_or_create(user=instance)
        if not created:
            student_profile.save()

@receiver(post_save, sender=CustomUser)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.is_teacher:
        TeacherProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_teacher_profile(sender, instance, **kwargs):
    if instance.is_teacher:
        teacher_profile, created = TeacherProfile.objects.get_or_create(user=instance)
        if not created:
            teacher_profile.save()


class PointCategory(models.Model):
    """ Category list for awarding points """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    point = models.PositiveIntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.point} pts"


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-category']

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

class AwardItem(models.Model):
    #gifts, textbooks, trips, etc
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_at', '-created_at')

    def __str__(self):
        return self.name

class RedeemAward(models.Model):
    select_award = models.ForeignKey(AwardItem, on_delete=models.CASCADE, null=True)
    date_redeemed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.select_award.name