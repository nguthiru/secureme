from django.contrib.auth.models import AbstractUser,BaseUserManager,AbstractBaseUser,PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.gis.db.models import PointField
from users.emails import send_approval_email
from users.entities import StationEntity
from neomodel.contrib.spatial_properties import NeomodelPoint,PointProperty
from shapely.geometry import Point
from neomodel import db

# class UserRoles(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()

#     def __str__(self) -> str:
#         return self.name
# # Create your models here.
class Station(models.Model):
    name = models.CharField(max_length=255)
    location = PointField(null=True,blank=True)
    def __str__(self) -> str:
        return self.name


@receiver(post_save, sender=Station)
def create_station_graph(sender, instance, created, **kwargs):
    # if created:
    query = """
    
        CREATE (a:Station {longitude:$longitude, latitude:$latitude, name: $name, entity_id: $entity_id})

    """
    results, meta = db.cypher_query(query, {'longitude':instance.location.x,'latitude':instance.location.y,'entity_id':instance.id,'name':instance.name}, resolve_objects=True)

    # location_point = NeomodelPoint(Point(instance.location.x,instance.location.y))
    # StationEntity(entity_id=instance.id, name=instance.name,location=location_point).save()


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

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    date_added = models.DateTimeField(auto_now_add=True)
    approved=models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=10)
    station = models.OneToOneField(Station, on_delete=models.CASCADE, null=True, blank=True)
    activated=models.BooleanField(default=False)
    # user_type = models.ForeignKey(UserRoles, on_delete=models.CASCADE,)
    objects = CustomUserManager()

    def get_username(self) -> str:
        return self.email
    
    def __str__(self):
        return self.email

class ApprovalRequests(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True)
    user_type = models.CharField(choices=CustomUser.USER_TYPE_CHOICES, max_length=10,default='analytics')
    work_id = models.CharField(max_length=255,null=True,blank=True)
    approve = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.user.email
@receiver(post_save, sender=ApprovalRequests)
def approve_user(sender, instance, created, **kwargs):
    if instance.approve:
        instance.user.approved = True
        instance.user.user_type = instance.user_type
        if instance.user_type == 'police':
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