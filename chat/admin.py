from django.contrib import admin

from .models import User, SingleChat, Messages
# Register your models here.

admin.site.register(User)
admin.site.register(SingleChat)
admin.site.register(Messages)
