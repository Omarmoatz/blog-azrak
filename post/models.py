from django.db import models

from users.models import CustomUser


class Post(models.Model):
    author = models.ForeignKey( CustomUser, on_delete=models.CASCADE, related_name='post_author')
    title = models.CharField( max_length=500)
    description = models.TextField(max_length=2000, blank=True, null=True)
    image = models.ImageField( upload_to='post_image/', blank=True, null=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return f'title: {self.title}'
    
    class Meta:
        ordering = ('created_at', )
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    user= models.ForeignKey( CustomUser, on_delete=models.CASCADE, related_name='user_post')
    post = models.ForeignKey( Post, on_delete=models.CASCADE, related_name='comment_post')
    content = models.TextField(max_length=900)
    created_at = models.DateTimeField( auto_now_add=True)
    parent = models.ForeignKey("self", related_name='replies', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user}---{str(self.post.title)}---{self.content}'
    
    class Meta:
        ordering = ('created_at', )
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'