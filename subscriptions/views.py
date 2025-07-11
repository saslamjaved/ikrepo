import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import SubscriptionPlan, UserSubscription
from django.utils import timezone
from datetime import timedelta

stripe.api_key = settings.STRIPE_SECRET_KEY

def subscription_plans(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/subscription_plans.html', {'plans': plans})

def create_checkout_session(request, plan_id):
    plan = SubscriptionPlan.objects.get(id=plan_id)
    
    # Create a Stripe Checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': plan.name,
                },
                'unit_amount': int(plan.price * 100),  # Stripe expects amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('subscription_success', args=[plan.id])),
        cancel_url=request.build_absolute_uri(reverse('subscription_plans')),
    )

    return redirect(session.url, code=303)

def subscription_success(request, plan_id):
    plan = SubscriptionPlan.objects.get(id=plan_id)
    
    # Handle post-payment logic: create or update the user's subscription
    subscription, created = UserSubscription.objects.get_or_create(user=request.user)
    subscription.plan = plan
    subscription.start_date = timezone.now()
    subscription.end_date = timezone.now() + timedelta(days=plan.duration_in_days)
    subscription.is_active = True
    subscription.save()

    return render(request, 'subscriptions/subscription_success.html', {'plan': plan})


from django.shortcuts import redirect

def gold_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        user_subscription = UserSubscription.objects.filter(user=request.user, plan__name='gold', is_active=True).exists()
        if not user_subscription:
            return redirect('subscription_plans')
        return view_func(request, *args, **kwargs)
    return wrapper_func

from django.contrib.auth.decorators import login_required
from .decorators import gold_required

@login_required
@gold_required
def gold_content(request):
    return render(request, 'subscriptions/gold_content.html')
