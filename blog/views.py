from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment, Share, Reply
from .forms import ArticleForm, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count
from .tasks import send_article_creation_email

####
from django.http import JsonResponse
from django.template.loader import render_to_string

def load_comments(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = Comment.objects.filter(article=article, is_approved=True).order_by('-created_at')
    comments_with_replies = {}
    for comment in comments:
        replies = Reply.objects.filter(comment=comment).order_by('-created_at')
        comments_with_replies[comment] = replies

    html = render_to_string('blog/comments_list.html', {
        'comments_with_replies': comments_with_replies
    }, request=request)

    return JsonResponse({'html': html})

@login_required
def post_comment(request, slug):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            article = get_object_or_404(Article, slug=slug)
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid form submission'})

####

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'blog/article_list.html', {'articles': articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    comments = Comment.objects.filter(article=article, is_approved=True).order_by('-created_at')
    
    # Create a dictionary to hold comments and their replies
    comments_with_replies = {}
    for comment in comments:
        replies = Reply.objects.filter(comment=comment).order_by('-created_at')
        comments_with_replies[comment] = replies

    comment_form = CommentForm()
    reply_form = ReplyForm()

    if request.method == 'POST':
        if 'comment_form' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.article = article
                comment.author = request.user
                comment.save()
                return redirect('article_detail', slug=slug)
        elif 'reply_form' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                comment_id = request.POST.get('comment_id')
                reply.comment = get_object_or_404(Comment, id=comment_id)
                reply.author = request.user
                reply.save()
                return redirect('article_detail', slug=slug)
    else:
        comment_form = CommentForm()
        reply_form = ReplyForm()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comments':comments,
        'comments_with_replies': comments_with_replies,
        'comment_form': comment_form,
        'reply_form': reply_form,
    })

"""
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    t_articles = Article.objects.annotate(num_likes=models.Count('likes')).order_by('-num_likes')    
    #comments = article.comments.all().order_by('-created_at')[:5]
    comments = Comment.objects.filter(article=article, is_approved=True).order_by('-created_at')[:5]
    comments_with_replies = {}
    for comment in comments:
        replies = Reply.objects.filter(comment=comment).order_by('-created_at')
        comments_with_replies[comment] = replies
        if request.method == 'POST':
        form1 = ReplyForm(request.POST)
        if form1.is_valid():
            reply = form.save(commit=False)
            # You need to specify the comment and author for the reply
            reply.comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
            reply.author = request.user
            reply.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form1 = ReplyForm()

    if request.method == 'POST':
        form2 = CommentForm(request.POST)
        if form2.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form2 = CommentForm()
    return render(request, 'blog/article_detail.html', {'article': article, 'comments': comments, 'form1': form1, 'form2': form2, 't_articles': t_articles, 'comments_with_replies': comments_with_replies,})
"""
@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            send_article_creation_email.delay(article.id)
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/create_article.html', {'form': form})

def update_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=slug)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/update_article.html', {'form': form, 'article': article})


@login_required
def like_article(request, slug):
    if not request.user.is_authenticated:
        return redirect('users:login')  
    article = get_object_or_404(Article, slug=slug)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return redirect('article_detail', slug=slug)


@login_required
def share_article(request, slug):
    if not request.user.is_authenticated:
        return redirect('users:login') 
    article = get_object_or_404(Article, slug=slug)
    Share.objects.create(article=article, user=request.user)
    return redirect('article_detail', slug=slug)


def trending_articles(request):
    articles = Article.objects.annotate(num_likes=models.Count('likes')).order_by('-num_likes')
    return render(request, 'blog/trending_articles.html', {'articles': articles})

def recent_articles(request):
    articles = Article.objects.all().order_by('-created_at')[:10]
    return render(request, 'blog/recent_articles.html', {'articles': articles})


@login_required
def post_reply(request,slug, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.author = request.user
            reply.save()
            return redirect('article_detail', slug=slug)
    else:
        form = ReplyForm()

    return render(request, 'blog/post_reply.html', {'form': form, 'comment': comment})