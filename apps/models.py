from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save

# User(AbstractUser),
# Category, Blog, Comment, Like

class User(AbstractUser):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    
class Category(models.Model):
    name = models.CharField(max_length=100)

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    img_url = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to='profile_avatars/', 
        default='profile_avatars/default.jpg', 
        blank=True, 
        null=True
    )
    bio = models.TextField(max_length=500, blank=True)           # ixtiyoriy
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    # Profile modeliga
    total_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"

# Har bir yangi user yaratilganda avtomatik Profile yaratib berish
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
    



    