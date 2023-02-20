from django.db import models
# from django.contrib.auth import get_user_model

# from accounts.models import Profile
from django.urls import reverse


# Getting User model object
# User = get_user_model()


class Post(models.Model):
    """
    This is a class to define posts for blog app
    """

    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    status = models.BooleanField()
    category = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, null=True
    )

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
    published_dt = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_snippet(self):
        return self.content[:3]

    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name
