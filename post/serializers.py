from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.exceptions import PermissionDenied

from users.serializers import UserSerializer
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    # detail_url = serializers.HyperlinkedIdentityField(
    #     view_name='post_detail',
    #     lookup_field='pk'
    # )
    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at',)


class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    comment_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'

    def get_comment_count(self,obj):
        return obj.comment_post.all().count()
 


class PostAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ('author_id', )




class CommentRetrieveSerializer(serializers.ModelSerializer):
    # detail_url = serializers.SerializerMethodField( method_name='get_url')
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    # def get_url(self,obj):
    #     request = self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse('post:comment_retrive_update_delete', kwargs={'pk':obj.pk}, request=request)



class CommentCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        post_id = self.context['post_id']
        user = self.context['request'].user  
        validated_data['post_id'] = post_id  
        validated_data['user'] = user  
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        print(user)
        if instance.user != user:
            raise PermissionDenied("You do not have permission to update this comment.")
        return super().update(instance, validated_data)
    

