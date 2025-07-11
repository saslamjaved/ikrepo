from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

TOPICS = (
    ("Innovative Methods", "Innovative Methods"),
    ("Skills", "Skills"),
    ("Learning Paths", "Learning Paths"),
    ("Technology Tools","Technology Tools"),
    ("Robotics Trends","Robotics Trends"),
    ("Industry Benefits","Industry Benefits"),
    ("Course Selection","Course Selection"),
    ("Interactive Learning","Interactive Learning"),
    ("Certification Impact","Certification Impact"),
    ("Domain News","Domain News"),
)

class Article(models.Model):
    title = models.CharField(max_length=200)
    topic = models.CharField(choices=TOPICS, max_length=100, default=0)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', default='')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

@receiver(pre_save, sender=Article)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        # Ensure uniqueness of the slug
        # This is optional but recommended to avoid conflicts
        original_slug = instance.slug
        queryset = sender.objects.filter(slug__startswith=original_slug)
        if queryset.exists():
            counter = 1
            new_slug = f"{original_slug}-{counter}"
            while queryset.filter(slug=new_slug).exists():
                counter += 1
                new_slug = f"{original_slug}-{counter}"
            instance.slug = new_slug

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.author} on {self.article.title}"

class Share(models.Model):
    article = models.ForeignKey(Article, related_name='shares', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    comment = models.ForeignKey(Comment, related_name='replies', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]