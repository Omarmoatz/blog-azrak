from django.contrib import admin

from .models import Post,Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_filter= ('title', 'author')
    search_fields = ('author', 'title')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

