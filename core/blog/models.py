from django.db import models
from django.contrib.auth import get_user_model


# Getting User model object
User = get_user_model()


class Post(models.Model):
    """
    This is a class to define postsfor blog app
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    status = models.BooleanField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    
    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    published_dt = models.DateTimeField()
    
    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.name