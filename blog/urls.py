from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('article/<slug>/', views.article_detail, name='article_detail'),
    path('article/<slug>/edit', views.update_article, name='update_article'),
    path('article_new/', views.create_article, name='create_article'),
    path('article/<slug>/like/', views.like_article, name='like_article'),
    path('article/<slug>/share/', views.share_article, name='share_article'),
    path('trending/', views.trending_articles, name='trending_articles'),
    path('recent/', views.recent_articles, name='recent_articles'),
    path('article/<slug>/comment/<int:comment_id>/reply/', views.post_reply, name='post_reply'),

    # URL for loading comments via AJAX
    path('article/<slug:slug>/comments/', views.load_comments, name='load_comments'),
    
    # URL for posting a comment via AJAX
    path('article/<slug:slug>/post-comment/', views.post_comment, name='post_comment'),
]
