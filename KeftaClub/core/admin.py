from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
admin.site.register(Message)
admin.site.register(Room)

@admin.register(PostComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'post', 'created_on')
    list_filter = ('created_on',)
    search_fields = ('body',)

    #actions = ['approve_comments']

    #def approve_comments(self, request, queryset):
    #   queryset.update(active=True)
