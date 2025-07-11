from django.urls import path
from .views import subscription_plans, create_checkout_session, subscription_success

urlpatterns = [
    path('subscriptions/', subscription_plans, name='subscription_plans'),
    path('create-checkout-session/<int:plan_id>/', create_checkout_session, name='create_checkout_session'),
    path('subscription-success/<int:plan_id>/', subscription_success, name='subscription_success'),
]
