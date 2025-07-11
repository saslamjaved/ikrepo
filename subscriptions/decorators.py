# subscriptions/decorators.py

from django.http import HttpResponseForbidden
from functools import wraps

def gold_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.usersubscription.plan.name == 'gold':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You must have a Gold subscription to access this page.")
    return _wrapped_view
