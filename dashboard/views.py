from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from blog.models import Article, Comment, Share
from resources.models import Resource,Chapter
from blog.forms import ArticleForm, CommentForm, ReplyForm
from .forms import SearchForm
from django.db import models
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from subscriptions.models import UserSubscription


# Create your views here.

# views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q

def upload_file(request):
    if request.method == 'POST' and request.FILES:
        file = request.FILES['file']
        file_name = file.name
        file_content = file.read()
        file_path = default_storage.save(file_name, ContentFile(file_content))
        return HttpResponse(f'File uploaded to: {file_path}')
    return render(request, 'upload.html')

def search_articles(request):
    form = SearchForm(request.GET or None)
    articles = Article.objects.all()
    resources = Resource.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            articles = articles.filter(title__icontains=query)
            resources = resources.filter(title__icontains=query)

    return render(request, 'dashboard/components/search_results.html', {'form': form, 'articles': articles,"resources":resources})

def home(request):


    articles = Article.objects.all().order_by('-created_at')[:10]
    t_articles = Article.objects.annotate(num_likes=models.Count('likes')).order_by('-num_likes')    
    r_articles = Article.objects.all().order_by('-created_at')[:5]
    return render(request,'dashboard/home.html',{'articles': articles, 't_articles': t_articles,'r_articles': r_articles})   

def contactus(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate form data (basic validation)
        if not all([name, email, subject, message]):
            return render(request, 'pages/contactus.html', {'error': 'All fields are required.'})

        # Prepare email
        email_subject = f"Contact Form Submission: {subject}"
        email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        from_email = settings.DEFAULT_FROM_EMAIL
        from_name = "ikSaan.com"
        from_email_with_name = f"{from_name} <{from_email}>"
        recipient_list = [settings.DEFAULT_FROM_EMAIL]  # Adjust to the desired recipient(s)

        # Send email
        try:
            send_mail(email_subject, email_message, from_email_with_name, recipient_list, fail_silently=False)
            return render(request, 'pages/contactus.html', {'sent_message': 'Your message has been sent. Thank you!'})
        except Exception as e:
            print(f"Error sending email: {e}")
            return render(request, 'pages/contactus.html', {'error': 'There was an error sending your message. Please try again later.'})

    else:
        return render(request, 'pages/contactus.html')  

def wwo(request):
    return render(request, 'pages/whatweoffer.html')
    
def aboutus(request):
    return render(request, 'pages/aboutus.html')   

def faq(request):
    return render(request, 'pages/pages_faq.html')    

def tandc(request):
    return render(request, 'pages/terms_conditions.html')  

def ccg(request):
    return render(request,'pages/ccg.html')     


def ai_test(request):
    return render(request,'pages/ai_test.html')    

from django.views.generic import TemplateView


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"


class adsTxtView(TemplateView):
    template_name = "ads.txt"
    
##########################
######## Mgmt ############

@user_passes_test(lambda u: u.is_superuser)
def blog_mgmt(request):
    articles = Article.objects.all()
    comments = Comment.objects.all()

    if request.method == 'POST':
        if 'approve_article' in request.POST:
            article_id = request.POST.get('article_id')
            article = get_object_or_404(Article, id=article_id)
            article.is_approved = True
            article.save()
        elif 'disapprove_article' in request.POST:
            article_id = request.POST.get('article_id')
            article = get_object_or_404(Article, id=article_id)
            article.is_approved = False
            article.save()
        elif 'approve_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            comment.is_approved = True
            comment.save()
        elif 'disapprove_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            comment.is_approved = False
            comment.save()
        elif 'delete_article' in request.POST:
            article_id = request.POST.get('article_id')
            article = get_object_or_404(Article, id=article_id)
            article.delete()
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)
            comment.delete()
        elif 'create_article' in request.POST:
            form = ArticleForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('blog_mgmt')
        elif 'update_article' in request.POST:
            article_id = request.POST.get('article_id')
            article = get_object_or_404(Article, id=article_id)
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('blog_mgmt')

    article_form = ArticleForm()
    return render(request, 'mgmt/blog_mgmt.html', {
        'articles': articles,
        'comments': comments,
        'article_form': article_form,
    })   


    ##############################################################
    ############          Resources Pages             ############
    ##############################################################

def pages_error_404(request,exception=None):
    return render(request,'pages/pages_error_404.html', status=404)


def ai_home(request):
    return render(request,'r/ai_home/ai_home.html')
def ai_learn(request):
    return render(request,'r/ai_learn/ai_learn.html')
def ai_projects(request):
    icArticle = Article.objects.filter(title="Image Classification")
    saArticle = Article.objects.filter(title="Sentiment Analysis")
    larsArticle = Article.objects.filter(title="Learn AI Recommendation Systems")
    lpaArticle = Article.objects.filter(title="Learn Predictive Analytics")
    lavArticle = Article.objects.filter(title="Learn Autonomous Vehicles")
    context={
        'ic':icArticle,
        'sa':saArticle,
        'lars':larsArticle,
        'lpa':lpaArticle,
        'lav':lavArticle,
    }
    return render(request,'r/ai_projects/ai_projects.html',{"context":context})
def ai_resources(request):
    return render(request,'r/ai_resources/ai_resources.html')
def ai_c_s(request):
    return render(request,'r/ai_c_s/ai_c_s.html')
def ai_blogs(request):
    return render(request,'r/ai_blogs/ai_blogs.html')     
def icArticle(request):
    return render(request,'r/ai_pages/ic.html')                                           
def saArticle(request):
    return render(request,'r/ai_pages/sa.html')
def larsArticle(request):
    return render(request,'r/ai_pages/lars.html')
def lpaArticle(request):
    return render(request,'r/ai_pages/lpa.html')
def lavArticle(request):
    return render(request,'r/ai_pages/lav.html')  
def chatbotsArticle(request):
    return render(request,'r/ai_pages/chatbots.html')    

def tnfArticle(request):
    return render(request,'r/ai_pages/tnf.html')  
def code_repoArticle(request):
    return render(request,'r/ai_pages/code_repo.html')   

def ml(request):
    return render(request,'r/ai_pages/ml.html')  
def dl(request):
    return render(request,'r/ai_pages/dl.html')   
def nlp(request):
    return render(request,'r/ai_pages/nlp.html')  
def cv(request):
    return render(request,'r/ai_pages/cv.html')
def ai_tutorials(request):
    return render(request,'r/ai_projects/ai_tutorials.html')   


"""
def google_site_verf():
    return render_template("dashboard/google-provided.html")                              
"""

import requests
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        user_message = body.get("message")
        sender_id = body.get("sender")

        if not user_message:
            return JsonResponse({"error": "Message is required"}, status=400)

        # Forward the message to the Rasa server
        rasa_url = "http://13.234.118.53:5005/webhooks/rest/webhook"
        response = requests.post(rasa_url, json={"sender": sender_id, "message": user_message})

        if response.status_code == 200:
            rasa_response = response.json()
            return JsonResponse({"messages": rasa_response}, safe=False)
        else:
            return JsonResponse({"error": "Error connecting to Rasa"}, status=response.status_code)

    return JsonResponse({"error": "Invalid request method"}, status=400)


"""
import requests
from django.http import JsonResponse

RASA_SERVER_URL = "http://13.201.229.216:5005/webhooks/rest/webhook"

def chatbot_response(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        sender_id = request.POST.get("sender")  # Unique user identifier
        payload = {
            "sender": sender_id,
            "message": user_message,
        }
        try:
            response = requests.post(RASA_SERVER_URL, json=payload)
            response_data = response.json()
            # Return the Rasa response to the frontend
            return JsonResponse({"messages": response_data}, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)
"""
from django.shortcuts import render


import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def chat(request):
    return render(request,"dashboard/chat.html")
    
@csrf_exempt
def chatbot_page(request):
    if request.method == 'POST':  # Ensure that it only processes POST requests
        message = json.loads(request.body).get('message')
        if not message:
            return JsonResponse({"error": "No message provided"}, status=400)
        
        rasa_api_url = "http://13.201.229.216:5005/webhooks/rest/webhook"
        
        # Send the message to the Rasa API
        response = requests.post(rasa_api_url, json={"message": message})
        
        if response.status_code == 200:
            rasa_response = response.json()
            return JsonResponse({"response": rasa_response})
        else:
            return JsonResponse({"error": "Error from Rasa API"}, status=500)
    
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)  # 405 for invalid HTTP method

#def chatbot_page(request):
#    return render(request, "dashboard/chat.html")
