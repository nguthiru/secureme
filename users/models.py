from django.contrib.auth.models import AbstractUser,BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.emails import send_approval_email
# class UserRoles(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()

#     def __str__(self) -> str:
#         return self.name
# # Create your models here.
class Station(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return self.name

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Normalize email address
        email = self.normalize_email(email)
        
        # Create and save the user
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Create a superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('police', 'Police Station'),
        ('analytics', 'Analytics Team'),
        ('admin','Admin')
    )
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    approved=models.BooleanField(default=False)
    REQUIRED_FIELDS = ['username','approved']
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=10)
    station = models.OneToOneField(Station, on_delete=models.CASCADE, null=True, blank=True)
    activated=models.BooleanField(default=False)
    # user_type = models.ForeignKey(UserRoles, on_delete=models.CASCADE,)
    objects = CustomUserManager()

class ApprovalRequests(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    approve = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.user.username
@receiver(post_save, sender=ApprovalRequests)
def approve_user(sender, instance, created, **kwargs):
    if instance.approve:
        instance.user.approved = True
        if instance.user.user_type == 'police':
            instance.user.station = instance.station
        instance.user.save()
        #send email to user
        send_approval_email(instance.user)


class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    reset_code = models.IntegerField()
    is_valid = models.BooleanField(default=False)
    code_used = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    grant_token = models.CharField(max_length=255,default="")

    def __str__(self) -> str:
        return self.user.email

class ValidationEmailCodes(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    code = models.IntegerField()
    code_used = models.BooleanField(default=False)
    is_valid = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    grant_token = models.CharField(max_length=255,default="")

    def __str__(self) -> str:
        return self.user.email