from django.contrib import admin

from users.models import CustomUser,ApprovalRequests,Station

# Register your models here.
admin.site.register([CustomUser,ApprovalRequests,Station])