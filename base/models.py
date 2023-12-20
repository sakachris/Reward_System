from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


# Define a custom user model that extends AbstractUser
class CustomUser(AbstractUser):
    """ customizing the user model """
    # Additional fields for the custom user model
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # String representation of the user object, used for display purposes
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Define a model for storing additional data related to students
class StudentProfile(models.Model):
    """ model for storing student's extra data """
    # Establish a one-to-one relationship with the CustomUser model
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                primary_key=True)
    
    # Additional fields for student-specific data
    grade = models.CharField(max_length=10, null=True, blank=True)
    adm_no = models.PositiveIntegerField(null=True, blank=True, unique=True)
    parent_contact = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.user.username


# Define a model for storing additional data related to teachers
class TeacherProfile(models.Model):
    """ model for storing teacher's extra data """
    # Establish a one-to-one relationship with the CustomUser model
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE,
                                primary_key=True)
    
    # Additional fields for teacher-specific data
    designation = models.CharField(max_length=30, null=True, blank=True)
    reg_no = models.PositiveIntegerField(null=True, blank=True, unique=True)
    contact = models.CharField(max_length=15, null=True, blank=True)


# Signal handler to create a StudentProfile when
# a CustomUser is created and is a student
@receiver(post_save, sender=CustomUser)
def create_student_profile(sender, instance, created, **kwargs):
    """Create a StudentProfile when a CustomUser is created & is a student"""
    if created and instance.is_student:
        StudentProfile.objects.get_or_create(user=instance)


# Signal handler to save a StudentProfile when
# a CustomUser is saved and is a student
@receiver(post_save, sender=CustomUser)
def save_student_profile(sender, instance, **kwargs):
    """Save a StudentProfile when a CustomUser is saved and is a student."""
    if instance.is_student:
        student_profile, created = (
                StudentProfile.objects.get_or_create(user=instance)
        )
        if not created:
            student_profile.save()


# Signal handler to create a TeacherProfile when
# a CustomUser is created and is a teacher
@receiver(post_save, sender=CustomUser)
def create_teacher_profile(sender, instance, created, **kwargs):
    """Create a TeacherProfile when a CustomUser is created & is a teacher"""
    if created and instance.is_teacher:
        TeacherProfile.objects.create(user=instance)


# Signal handler to save a TeacherProfile when
# a CustomUser is saved and is a teacher
@receiver(post_save, sender=CustomUser)
def save_teacher_profile(sender, instance, **kwargs):
    """Save a TeacherProfile when a CustomUser is saved and is a teacher"""
    if instance.is_teacher:
        teacher_profile, created = (
                TeacherProfile.objects.get_or_create(user=instance)
        )
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


# Signal handler to set the teacher field in PointTransaction before saving
@receiver(pre_save, sender=PointTransaction)
def set_teacher(sender, instance, **kwargs):
    """Set the teacher field in PointTransaction before saving"""

    # Check if the teacher_id is not set
    if not instance.teacher_id:
        # Retrieve the user model and get the current user by primary key
        current_user = get_user_model().objects.get(pk=instance.teacher_id)
        # Check if the current user is authenticated and is a teacher
        if (
            current_user and
            current_user.is_authenticated and
            current_user.is_teacher
        ):
            # Set the teacher field in PointTransaction to the current user
            instance.teacher = current_user


# Define a model for AwardItem to be redeemed by students
class AwardItem(models.Model):
    """ gifts, textbooks, trips, etc """
    name = models.CharField(max_length=100)
    points = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    units = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Specify the default ordering for queries
        ordering = ('-updated_at', '-created_at')

    # String representation of the AwardItem object, used for display purposes
    def __str__(self):
        return f"{self.name} - {self.points} points - {self.units} remaining"


class RedeemAward(models.Model):
    """ model for redeeming award """
    select_award = models.ForeignKey(
        AwardItem,
        on_delete=models.CASCADE,
        null=True,
        limit_choices_to={'units__gt': 0}
    )
    student = models.ForeignKey(
        CustomUser,
        related_name='redeeming_point',
        on_delete=models.CASCADE,
        limit_choices_to={'is_student': True}
    )
    date_redeemed = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_redeemed']

    def __str__(self):
        return self.select_award.name

    def save(self, *args, **kwargs):
        # Ensuring atomicity when updating both AwardItem and RedeemAward
        with transaction.atomic():
            # Deduct points from units when saving a new RedeemAward instance
            if not self.pk:  # Check if the instance is being created
                self.select_award.units -= 1
                self.select_award.save()

            super().save(*args, **kwargs)
