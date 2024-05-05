from django.contrib import admin
from .models import Profile, Course, Post


# Register your models here.
admin.site.register(Course)
admin.site.register(Post)
admin.site.register(Profile)
