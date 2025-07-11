"""
URL configuration for ikSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_articles, name='search_articles'),    
    path('aboutus', views.aboutus, name='aboutus'),
    path('contactus', views.contactus, name='contactus'),
    path('whatweoffer', views.wwo, name='wwo'),
    path('faq', views.faq, name='faq'),
    path('termsandconditions', views.tandc, name='tandc'), 
    path('blog_mgmt', views.blog_mgmt, name='blog_mgmt'),
    path('ccg', views.ccg, name='ccg'),

    #### resources URL's ####
    path('ai_home', views.ai_home, name='ai_home'),
    path('ai_learn', views.ai_learn, name='ai_learn'),
    path('ai_p_t', views.ai_projects, name='ai_projects'),
    path('ai_resources', views.ai_resources, name='ai_resources'),
    path('ai_c_s', views.ai_c_s, name='ai_c_s'),
    path('ai_test', views.ai_test, name='ai_test'),
    path('ai_blogs', views.ai_blogs, name='ai_blogs'),

    path('icArticle', views.icArticle, name='icArticle'),
    path('saArticle', views.saArticle, name='saArticle'),        
    path('larsArticle', views.larsArticle, name='larsArticle'),
    path('lpaArticle', views.lpaArticle, name='lpaArticle'),
    path('lavArticle', views.lavArticle, name='lavArticle'),
    path('chatbotsArticle', views.chatbotsArticle, name='chatbotsArticle'),
    path('tnfArticle', views.tnfArticle, name='tnfArticle'),
    path('code_repoArticle', views.code_repoArticle, name='code_repoArticle'),  
    path('ml', views.ml, name='ml'),
    path('dl', views.dl, name='dl'),
    path('nlp', views.nlp, name='nlp'),
    path('cv', views.cv, name='cv'),   
    path('ai_tutorials', views.ai_tutorials, name='ai_tutorials'),          
    path("chatbot/", views.chatbot_response, name="chatbot"),
    path("chat/", views.chat, name="chat"),

    path("robots.txt", views.RobotsTxtView.as_view(content_type="text/plain"), name="robots"),
    path("ads.txt", views.adsTxtView.as_view(content_type="text/plain"), name="ads"),
]
