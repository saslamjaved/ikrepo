from django.shortcuts import render,get_object_or_404, redirect
from subscriptions.models import SubscriptionPlan, UserSubscription
from .models import Resource,Chapter,Lesson

from django.http import HttpResponseForbidden
from django.db.models import Q
from django.db import models
from django.utils import timezone


def resource_list(request):
    resources = Resource.objects.all()
    context = {
    'resources':resources,
    }
    return render(request, 'resources/resource_list.html', context)

def resource_list1(request):
    # Get all resources
    resources = Resource.objects.all()

    if not request.user.is_authenticated:
        return redirect('users:login')

    # Fetch the user's active subscription
    user_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    user_plan = user_subscription.plan.name if user_subscription and user_subscription.plan else None
    # Filter resources based on the user's subscription level
    if user_plan == 'gold':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='gold') | 
            Q(minimum_subscription_plan='silver') | 
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) | 
            Q(is_demo=True)
        )
    elif user_plan == 'silver':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='silver') | 
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) | 
            Q(is_demo=True)
        )
    elif user_plan == 'bronze':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) | 
            Q(is_demo=True)            
        )
        print("Minimum subscriion is :" ,accessible_resources)
    else:
        # If no active subscription or no plan, only show free and demo resources
        accessible_resources = resources.filter(Q(is_free=True) | Q(is_demo=True))

    free_resources = resources.filter(is_free=True).values_list('title', flat=True)
    
    context = {
        'user_plan': user_plan,
        'accessible_resources': accessible_resources,
        'free_resources': free_resources,
    }

    return render(request, 'resources/resource_list.html', context)


def resource_detail(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    chapters = resource.chapters.all()  # Get all chapters for this resource
    #chapter = chapters.values_list('file_name', flat=True).first()

    if not request.user.is_authenticated:
        return redirect('users:login')
    #####################################
    resources = Resource.objects.all()
    user_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    
    user_plan = user_subscription.plan.name if user_subscription and user_subscription.plan else None    

    if user_plan == 'gold':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='gold') | 
            Q(minimum_subscription_plan='silver') | 
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) 
        ).values_list('title',flat=True)
    elif user_plan == 'silver':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='silver') | 
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) 
        ).values_list('title',flat=True)
    elif user_plan == 'bronze':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True)           
        ).values_list('title',flat=True)
        #print("Minimum subscriion is :" ,accessible_resources)
    else:
        # If no active subscription or no plan, only show free and demo resources
        accessible_resources = resources.filter(Q(is_free=True)).values_list('title',flat=True)

  
    r_list=[]
    for r in accessible_resources:
        r_list.append(r)
    
    if str(resource) in r_list:
        print("True")
        user_has_access=True
    else:
        print("False")
        user_has_access=False
    
    print("r_list",r_list)
    print("user_has_access",user_has_access)
    """
    chapter = chapters.values_list('title',flat=True).first()        
    print("@@@@@@@@@@@@@@@")
    print("accessible_resources",accessible_resources)
    print("r_list",r_list)
    print("resource : ", resource)
    print("resource datatype : ", type(resource))
    print("user_has_access : ",user_has_access)
    print("@@@@@@@@@@@@@@@")
    #####################################
    #chapter = chapters.values('file_name').first()
    """
    chapter = chapters.values().first()
    # Check if the user can access the resource
    if not is_accessible(request.user, slug):
        return redirect('subscription_plans')

    # Fetch lessons for the selected chapter if provided
    chapter_slug = request.GET.get('chapter')  # Get the chapter slug from query params
    selected_chapter = None
    lessons = []

    if chapter_slug:
        selected_chapter = get_object_or_404(Chapter, slug=chapter_slug, resource=resource)
        lessons = selected_chapter.lessons.all()  # Get all lessons for the selected chapter

    context = {
        'resource': resource,
        'chapters': chapters,
        'chapter': chapter,
        'selected_chapter': selected_chapter,
        'lessons': lessons,
        'user_has_access':user_has_access,  
    }
    return render(request, 'resources/resource_detail.html', context)

def chapter_detail(request, slug):

    if not request.user.is_authenticated:
        return redirect('users:login')

    chapter=get_object_or_404(Chapter,slug=slug)
    resource = chapter.resource
    chapters = resource.chapters.all()
    chapter_det=Chapter.objects.filter(slug=slug).values()
    resources = Resource.objects.all()
    
    user_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    
    user_plan = user_subscription.plan.name if user_subscription and user_subscription.plan else None    

    if user_plan == 'gold':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='gold') | 
            Q(minimum_subscription_plan='silver') | 
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) 
        ).values_list('title',flat=True)
    elif user_plan == 'silver':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='silver') | 
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) 
        ).values_list('title',flat=True)
    elif user_plan == 'bronze':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True)           
        ).values_list('title',flat=True)
        #print("Minimum subscriion is :" ,accessible_resources)
    else:
        # If no active subscription or no plan, only show free and demo resources
        accessible_resources = resources.filter(Q(is_free=True)).values_list('title',flat=True)

    r_list=[]
    for r in accessible_resources:
        r_list.append(r)
    
    if str(resource) in r_list:
        print("True")
        user_has_access=True
    else:
        print("False")
        user_has_access=False

    #resource_names = accessible_resources[1]
    print("r_list",r_list)
    print("user_has_access",user_has_access)


    chapter_slug = request.GET.get('chapter')  # Get the chapter slug from query params
    selected_chapter = None
    lessons = []
    cs = chapter_det.values_list('id').first()
    c=cs
    lessons = Lesson.objects.filter(chapter=c).values()
    if chapter_slug:
        selected_chapter = get_object_or_404(Chapter, slug=chapter_slug, resource=resource)
        lessons = selected_chapter.lessons.all()  # Get all lessons for the selected chapter
    
    """
    #lessons = Chapter.lessons.filter(title=chapter.title).values()
    print("{{{{{{{{{{{}}}}}}}}}}}")
    print("c",c[0])
    print("chapter_slug",chapter_slug)
    print("selected_chapter",selected_chapter)
    print("lessons", chapter.resource.title)
    #print("Resource names",resource_names)
    #print("{{{{{{{{{{{}}}}}}}}}}}")
    """
    context = {
        'chapter':chapter,
        'chapter_det':chapter_det,
        'lessons':lessons,
        'Resource':Resource,
        'user_has_access':user_has_access,
    }

    return render(request, 'resources/chapter_detail.html', context)
    
"""
def chapter_detail(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    chapter = get_object_or_404(Chapter, slug=slug)
    #chapters = resource.chapters.all()  # Get all chapters for this resource
    #chapter = chapters.values_list('file_name', flat=True).first()

    #chapter = chapters.values('file_name').first()
    #chapter = chapters.values().first()
    
#    print("First Chapter : ", chapter)
    # Check if the user can access the resource
#    if not is_accessible(request.user, slug):
#        return HttpResponseForbidden("You do not have permission to access this resource.")

    # Fetch lessons for the selected chapter if provided
    chapter_slug = request.GET.get('chapter')  # Get the chapter slug from query params
#    selected_chapter = None
    lessons = []

    if chapter_slug:
        selected_chapter = get_object_or_404(Chapter, slug=chapter_slug, resource=resource)
        lessons = selected_chapter.lessons.all()  # Get all lessons for the selected chapter

    context = {
        'resource': resource,
        'chapters': chapters,
        'chapter': chapter,
        'selected_chapter': selected_chapter,
        'lessons': lessons
    }
    return render(request, 'resources/chapter_detail.html', context)
"""
"""
def resource_detail(request, slug):
    resource = get_object_or_404(Resource, slug=slug)

    if not is_accessible(request.user, slug):
        return HttpResponseForbidden("You do not have permission to access this resource.")
    
    return render(request, 'resources/resource_detail.html', {'resource': resource})
"""

def is_accessible(user, slug):
    # Check if the resource is free
    resource = Resource.objects.get(slug=slug)
    if resource.is_free or resource.is_demo:
        return True

    # Check if the user has an active subscription
    if user.is_authenticated:
        try:
            user_subscription = UserSubscription.objects.get(user=user, is_active=True)
            user_plan = user_subscription.plan.name

            # Get the minimum subscription level for the resource
            resource_plan = resource.minimum_subscription_plan

            # Gold can access everything, Silver can access Silver and below, Bronze can access Bronze only
            if user_plan == 'gold' or \
               (user_plan == 'silver' and resource_plan in ['silver', 'bronze']) or \
               (user_plan == 'bronze' and resource_plan == 'bronze'):
                return True
        except UserSubscription.DoesNotExist:
            pass
    
    return False











"""
def resource_list(request):
    # Get all resources
    resources = Resource.objects.all()

    if not request.user.is_authenticated:
        return redirect('users:login')

    # Fetch the user's active subscription
    user_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    # Get the plan details or set a default message
    plan_details = user_subscription.plan if user_subscription else None
    
    if plan_details:
        user_resources = Resource.objects.filter(minimum_subscription_plan=plan_details)
   
    else:
        user_resources = Resource.objects.none()  # No resources if plan does not exist
    
    free_resources = Resource.objects.filter(is_free=True).values_list('title',flat=True)
    context = {
            'resources':resources,
            'user_resources':user_resources,
            'free_resources':free_resources
    } 
    print(resources)
    return render(request, 'resources/resource_list.html', context)

# resources/views.py

from django.shortcuts import render, get_object_or_404
from .models import Resource

def resource_detail(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    if not is_accessible(request.user,slug):
        return HttpResponseForbidden("You do not have permission to access this resource.")
    
    return render(request, 'resources/resource_detail.html', {'resource': resource})


def is_accessible(user,slug):
    is_free = False
    # Free resources are always accessible
    is_free = Resource.objects.filter(slug=slug, is_free=True).first()
    if is_free:
        return True
    
    # Check if the user has an active subscription
    if user.is_authenticated:
        try:
            user_subscription = UserSubscription.objects.get(user=user, is_active=True)
            resource_subscription_plan=Resource.objects.filter(slug=slug).values_list('minimum_subscription_plan',flat=True).first()
            if user_subscription.plan.name == resource_subscription_plan:
                return True
        except UserSubscription.DoesNotExist:
            pass
    
    # Otherwise, the resource is not accessible
    return False
"""
####################  Test environment #############################################
def tr_list(request):
    resources = Resource.objects.all()
    context = {
    'resources':resources,
    }
    return render(request, 't/tr_list.html', context)


def tl_detail(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    
    # Fetch all chapters related to the resource
    chapters = resource.chapters.all()
    #lessons=chapters.lesson.all()

    # Attach lessons to each chapter
    #for chapter in chapters:
    #    chapter.lessons = chapter.lessons.all()  # Get lessons for each chapter

    context = {
        'resource': resource,
        'chapters': chapters,  # Pass chapters with their lessons attached
    }

    return render(request, 't/tl_detail.html', context)


from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Lesson



def get_lesson_pages_by_slug(request, lesson_slug):
    lesson = get_object_or_404(Lesson, slug=lesson_slug)
    pages_list = lesson.pages.all().order_by('order')  # Ensure pages are ordered

    # Pagination
    paginator = Paginator(pages_list, 1)  # Show 5 pages per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    pages_data = []
    for page in page_obj.object_list:
        page_info = {
            'title': page.title,
            'content_type': page.content_type,
            'content': page.content,
            'image': page.image.url if page.image else None,
            'video_url': page.video_url,
            'quiz_id': page.quiz.id if page.quiz else None
        }
        pages_data.append(page_info)
    print("{{{{{{{{{{{}}}}}}}}}}}")
    print("pages_data",pages_data)
    print("{{{{{{{{{{{}}}}}}}}}}}")

    response = {
        'pages': pages_data,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
    }
    return JsonResponse(response)



"""
def tl_detail(request, slug):
    resource = get_object_or_404(Resource, slug=slug)
    chapters = resource.chapters.all()

    if not is_accessible(request.user, slug):
        return HttpResponseForbidden("You do not have permission to access this resource.")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        chapter_slug = request.GET.get('chapter')
        lesson_slug = request.GET.get('lesson')
        mark_complete = request.GET.get('mark_complete') == 'true'
        progress_percentage = float(request.GET.get('progress_percentage', 0))

        selected_chapter = get_object_or_404(Chapter, slug=chapter_slug, resource=resource) if chapter_slug else None
        selected_lesson = get_object_or_404(Lesson, slug=lesson_slug, chapter=selected_chapter) if lesson_slug else None

        if mark_complete and selected_lesson:
            LessonCompletion.objects.update_or_create(
                user=request.user, lesson=selected_lesson,
                defaults={'completed_at': timezone.now(), 'progress_percentage': progress_percentage}
            )

        next_lesson = None
        if selected_lesson:
            next_lessons = selected_chapter.lessons.filter(order__gt=selected_lesson.order).order_by('order')
            if next_lessons.exists():
                next_lesson = next_lessons.first()

        completed_percentage = LessonCompletion.objects.filter(user=request.user, lesson__in=selected_chapter.lessons.all()).aggregate(models.Avg('progress_percentage'))['progress_percentage__avg'] or 0

        data = {
            'chapter_title': selected_chapter.title if selected_chapter else '',
            'title': selected_lesson.title if selected_lesson else '',
            'content': selected_lesson.content if selected_lesson else '',
            'order': selected_lesson.order if selected_lesson else '',
            'next_lesson': {
                'slug': next_lesson.slug if next_lesson else '',
                'title': next_lesson.title if next_lesson else ''
            } if next_lesson else None,
            'completed_percentage': completed_percentage
        }
        return JsonResponse(data)

    # Regular request handling for full page loads
    chapter_slug = request.GET.get('chapter')
    selected_chapter = None
    lessons = []
    selected_lesson = None

    if chapter_slug:
        selected_chapter = get_object_or_404(Chapter, slug=chapter_slug, resource=resource)
        lessons = selected_chapter.lessons.all()

        lesson_slug = request.GET.get('lesson')
        if lesson_slug:
            selected_lesson = get_object_or_404(Lesson, slug=lesson_slug, chapter=selected_chapter)

    print("selected_chapter",selected_chapter)
    context = {
        'resource': resource,
        'chapters': chapters,
        'selected_chapter': selected_chapter,
        'lessons': lessons,
        'selected_lesson': selected_lesson
    }
    return render(request, 't/tl_detail.html', context)
"""

"""
def tl_detail(request, slug):

    if not request.user.is_authenticated:
        return redirect('users:login')

    chapter=get_object_or_404(Chapter,slug=slug)
    chapter_det=Chapter.objects.filter(slug=slug).values()
    resources = Resource.objects.all()
    user_subscription = UserSubscription.objects.filter(user=request.user, is_active=True).first()
    
    user_plan = user_subscription.plan.name if user_subscription and user_subscription.plan else None    

    if user_plan == 'gold':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='gold') | 
            Q(minimum_subscription_plan='silver') | 
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) | 
            Q(is_demo=True)
        )
    elif user_plan == 'silver':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='silver') | 
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) | 
            Q(is_demo=True)
        )
    elif user_plan == 'bronze':
        accessible_resources = resources.filter(
            Q(minimum_subscription_plan='bronze') | 
            Q(is_free=True) | 
            Q(is_demo=True)            
        ).values_list('title',flat=True)
        #print("Minimum subscriion is :" ,accessible_resources)
    else:
        # If no active subscription or no plan, only show free and demo resources
        accessible_resources = resources.filter(Q(is_free=True) | Q(is_demo=True)).first()

    #l=len(accessible_resources)
    print("Datatype of accessible_resources ",type(accessible_resources))
    r_list=[]
    for r in [accessible_resources]:
        r_list.append(r)
        
    #print(r_list)
    
    if str(chapter.resource.title) in r_list:
        print("True")
        user_has_access=True
    else:
        print("False")
        user_has_access=False

    #resource_names = accessible_resources[1]
    

    print("{{{{{{{{{{{}}}}}}}}}}}")
    #print("user_subscription",user_subscription)
    #print("user_plan",user_plan)
    print("accessible_resources",accessible_resources)
    #print("chapter.resource.title", chapter.resource.title)
    #print("Resource names",resource_names)
    #print("{{{{{{{{{{{}}}}}}}}}}}")
    chapter_slug = request.GET.get('chapter')  # Get the chapter slug from query params
    selected_chapter = None
    lessons = []

    if chapter_slug:
        selected_chapter = get_object_or_404(Chapter, slug=chapter_slug, resource=resource)
        lessons = selected_chapter.lessons.all()  # Get all lessons for the selected chapter

    context = {
        'chapter':chapter,
        'chapter_det':chapter_det,
        'lessons':lessons,
        'Resource':Resource,
        'user_has_access':user_has_access,
    }

    return render(request, 't/tl.html', context)
    """

    