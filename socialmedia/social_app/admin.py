from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AppUser)
admin.site.register(Address)
admin.site.register(Post)
admin.site.register(Image)

