from celery import shared_task
from django.core.mail import send_mail
from .models import Article

@shared_task
def send_article_creation_email(article_id):
    article = Article.objects.get(pk=article_id)
    send_mail(
        'New Article Created',
        f'Article "{article.title}" has been created.',
        'iksaangroups@gmail.com',
        ['saslamjaveed@gmail.com.com'],
        fail_silently=False,
    )
