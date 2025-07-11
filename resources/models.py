# resources/models.py

from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from django.utils import timezone
from subscriptions.models import SubscriptionPlan, UserSubscription

from django.db import models
from autoslug import AutoSlugField
from django.conf import settings
from django.utils import timezone
from subscriptions.models import SubscriptionPlan, UserSubscription

# Resource model
class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content_type = models.CharField(max_length=50, choices=[('article', 'Article'), ('video', 'Video')], default='article')
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False, default='')
    file_name = models.CharField(max_length=255, default="")
    thumbnail = models.ImageField(upload_to='thumbnails/', default='')
    is_free = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)
    minimum_subscription_plan = models.CharField(max_length=20, choices=[('gold', 'Gold'), ('silver', 'Silver'), ('bronze', 'Bronze')], blank=True, null=True)

    def can_user_access(self, user):
        if user.is_authenticated:
            if self.minimum_subscription_plan:
                user_subscription = UserSubscription.objects.filter(user=user, plan=self.minimum_subscription_plan).exists()
                return user_subscription
            return True
        return self.is_free

    def __str__(self):
        return self.title

# Chapter model
class Chapter(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_name = models.CharField(max_length=255, default="")
    order = models.PositiveIntegerField(default=1)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False, default='')
    is_demo = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.resource.title} - {self.title}'

    class Meta:
        ordering = ['order']

# Lesson model
class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False, default='')

    def __str__(self):
        return f'{self.chapter.title} - {self.title}'

    class Meta:
        ordering = ['order']

# User lesson completion tracking model
User = settings.AUTH_USER_MODEL

class LessonCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    progress_percentage = models.FloatField(default=0)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f'{self.user.username} - {self.lesson.title} - {self.progress_percentage}% completed'


class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Then update the Page model with the correct ForeignKey relation:
class Page(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
        ('quiz', 'Quiz'),
    ]

    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name='pages')
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES, default='text')
    content = models.TextField(blank=True, null=True)  # General content for text-based pages
    image = models.ImageField(upload_to='lesson_images/', blank=True, null=True)  # For image-based content
    video_url = models.URLField(blank=True, null=True)  # For video-based content
    quiz = models.ForeignKey('Quiz', on_delete=models.SET_NULL, blank=True, null=True)  # Optional quiz content
    order = models.PositiveIntegerField(default=1)  # Order of pages in the lesson
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False, default='')

    def __str__(self):
        return f'{self.lesson.title} - {self.title}'

    class Meta:
        ordering = ['order']

# User page completion tracking model
User = settings.AUTH_USER_MODEL

class PageCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    progress_percentage = models.FloatField(default=0)  # Track progress through the page

    class Meta:
        unique_together = ('user', 'page')

    def __str__(self):
        return f'{self.user.username} - {self.page.title} - {self.progress_percentage}% completed'



########################
"""
class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    content_type = models.CharField(max_length=50, choices=[('article', 'Article'), ('video', 'Video')], default='article')
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False,default='')
    file_name = models.CharField(max_length=255,default="")
    thumbnail = models.ImageField(upload_to='thumbnails/', default='')
    is_free = models.BooleanField(default=False)
    is_demo = models.BooleanField(default=False)
    minimum_subscription_plan = models.CharField(max_length=20, choices=[('gold', 'Gold'), ('silver', 'Silver'), ('bronze', 'Bronze')], blank=True, null=True)

    def can_user_access(self, user):
        if user.is_authenticated:
            # Check if there's a subscription plan
            if self.minimum_subscription_plan:
                # Filter for a subscription that matches the plan
                user_subscription = UserSubscription.objects.filter(user=user, plan=self.minimum_subscription_plan).exists()
                return user_subscription
            return True  # If no plan is required, allow access
        return self.is_free  # Allow access if the resource is marked as free

    def __str__(self):
        return self.title

class Chapter(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file_name = models.CharField(max_length=255,default="")
    order = models.PositiveIntegerField(default=1)  # Order of the chapter within the resource
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False,default='')  # Auto-slug    
    is_demo = models.BooleanField(default=False)  # Flag to indicate demo availability

    def __str__(self):
        return f'{self.resource.title} - {self.title}'

    class Meta:
        ordering = ['order']

class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()  # You can also use a rich text field or file field depending on the content
    order = models.PositiveIntegerField(default=1)  # Order of the lesson within the chapter
    slug = AutoSlugField(populate_from='title', unique=True, always_update=False,default='')  # Auto-slug    

    def __str__(self):
        return f'{self.chapter.title} - {self.title}'

    class Meta:
        ordering = ['order']

User = settings.AUTH_USER_MODEL
class LessonCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    progress_percentage = models.FloatField(default=0)  # Track progress percentage
    
    class Meta:
        unique_together = ('user', 'lesson')
        
    def __str__(self):
        return f'{self.user.username} - {self.lesson.title} - {self.progress_percentage}% completed'

"""