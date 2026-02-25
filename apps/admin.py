from django.contrib import admin
from .models import User, Category, Blog, Comment, Profile

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Profile)
