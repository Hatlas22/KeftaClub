from django.contrib import admin
from .models import Profile, Post, LikePost, FollowersCount, Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('body',)
    #actions = ['approve_comments']

    #def approve_comments(self, request, queryset):
    #   queryset.update(active=True)
