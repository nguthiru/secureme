from django.contrib.auth.models import AbstractUser
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


class CustomUser(AbstractUser):
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
    # user_type = models.ForeignKey(UserRoles, on_delete=models.CASCADE,)

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
