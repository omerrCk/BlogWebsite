from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    photo = models.ImageField(upload_to='blog_photos/%Y/%m/%d/',
                              blank=True)
    slug = models.SlugField(max_length=250,null=True,unique=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=False
                               )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT)
    likes = models.ManyToManyField(User, blank=True, related_name="blog_posts")

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def str(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug}) 
    
    def number_of_likes(self):
        return self.likes.count()
    





