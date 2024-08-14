from django.contrib import admin

from .models import Post,Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('author_id', 'title', 'created_at')
    list_filter= ('author_id', 'title')
    search_fields = ('author_id', 'title')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

