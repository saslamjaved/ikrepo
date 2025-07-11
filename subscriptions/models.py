from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class SubscriptionPlan(models.Model):
    PLAN_CHOICES = (
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
    )
    
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Price in USD
    description = models.TextField()
    access_to_resources = models.BooleanField(default=False)
    access_to_mentors = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    duration_in_days = models.PositiveIntegerField(default=30)  # Subscription duration (e.g., 30 days)

    def __str__(self):
        return self.name

class UserSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.plan.name if self.plan else 'No Plan'}"
