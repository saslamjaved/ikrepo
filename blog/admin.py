from django.contrib import admin
from .models import Article, Comment, Share, Reply

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'shared_at')

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1  # Number of empty reply forms to display by default

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created_at', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('content',)
    inlines = [ReplyInline]

class ReplyAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'created_at')

admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)