from django.contrib import admin
from admin_app.models import Message, UserSearchHistory

# Register your models here.
admin.site.register(Message)
admin.site.register(UserSearchHistory)