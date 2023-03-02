from django.contrib import admin

#import from the models that we previously have written
from .models import *

# # Register your models here.
admin.site.register(AppUser)