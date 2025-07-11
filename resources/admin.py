from django.contrib import admin
from .models import Resource, Chapter, Lesson, Page, PageCompletion, LessonCompletion, Quiz  # Import the Quiz model

# Inline for managing pages within the lesson admin
class PageInline(admin.TabularInline):
    model = Page
    extra = 1  # Number of empty page forms to display in admin

# Admin for Lesson model with pages inline
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'order')  # Fields to display in the list view
    list_filter = ('chapter',)  # Filters in the admin
    search_fields = ('title', 'chapter__title')  # Search by lesson and chapter title
    inlines = [PageInline]  # Display pages inline within lessons

# Admin for Page model
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'order', 'content_type')  # Fields to display
    list_filter = ('lesson', 'content_type')  # Filter by lesson and content type
    search_fields = ('title', 'lesson__title')  # Search by page title or lesson title

# Admin for Quiz model
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at')  # Fields to display for quiz
    search_fields = ('title',)  # Allow search by quiz title

# Admin for PageCompletion model
class PageCompletionAdmin(admin.ModelAdmin):
    list_display = ('user', 'page', 'completed_at', 'progress_percentage')  # Fields to display
    list_filter = ('user', 'page__lesson')  # Filters by user and lesson
    search_fields = ('user__username', 'page__title')  # Search by user or page title

class ChaptereAdmin(admin.ModelAdmin):
    list_display=('title',)
    list_filter= ('resource',)

# Register the models in the admin
admin.site.register(Resource)
admin.site.register(Chapter,ChaptereAdmin)
admin.site.register(Lesson, LessonAdmin)  # Register Lesson with customized admin
admin.site.register(Page, PageAdmin)  # Register Page with customized admin
admin.site.register(PageCompletion, PageCompletionAdmin)  # Register PageCompletion
admin.site.register(LessonCompletion)  # Register LessonCompletion
admin.site.register(Quiz, QuizAdmin)  # Register Quiz with its own admin
