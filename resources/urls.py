from django.urls import path
from .views import resource_list, resource_detail,chapter_detail,tr_list,tl_detail,get_lesson_pages_by_slug

urlpatterns = [
    path('resources/', resource_list, name='resource_list'),
    path('resources/<slug>/', resource_detail, name='resource_detail'),
    path('resource/<slug>/', chapter_detail, name='chapter_detail'),
    #path('resource/<slug>/', lesson_detail, name='lesson_detail'),
    ############ Test ########
    path('r/', tr_list, name='tr_list'),
    path('r/<slug>/', tl_detail, name='tl_detail'),
    path('r/<slug:lesson_slug>/pages/', get_lesson_pages_by_slug, name='get_lesson_pages_by_slug'),
]