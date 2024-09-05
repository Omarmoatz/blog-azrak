from rest_framework.response import Response
from rest_framework import generics, status, mixins
from django.shortcuts import get_object_or_404
from django.db.models.functions import Upper
from django.db.models import Count, Min, Max
from django.http import HttpResponse

from .models import Post, Comment
from .serializers import PostSerializer,PostDetailSerializer,PostAddSerializer, CommentRetrieveSerializer, CommentCreateSerializer, RepliesListSerializer

class PostApiView(generics.GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request,*args, **kwargs):
        pk =self.kwargs.get('pk')
        if pk:
            sigle_post = Post.objects.get(pk=pk)
            data= PostDetailSerializer(sigle_post).data
            return Response({'data':data})
        
        post = Post.objects.all()
        data = PostSerializer(post, many=True, context={'request': request}).data
        
        return Response({'data':data})

    def post(self, request, *args, **kwargs):
        user = self.request.user
        data = self.request.data
        serializer = PostAddSerializer(data=data)
        if serializer.is_valid():
            post = Post.objects.create(
                author_id = user,
                title = data['title'],
                description = data['description'],
                image = data['image'],
            )
            info = PostAddSerializer(post).data
            return Response({'detail':'succecfully_added',
                             'data':info})
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        data = self.request.data
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, id=pk)

        serializer = PostAddSerializer(data=data, instance=post, partial=True)
        if serializer.is_valid():

            serializer.save()

            info = PostAddSerializer(post).data
            return Response({'detail':'succecfully_updated',
                            'data':info})
        
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(PostApiView, id=pk)  
        post.delete()  
        return Response({'detail':'successfully_deleted'}, status=status.HTTP_204_NO_CONTENT)    




class CommentApiView(generics.GenericAPIView,
                     mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentRetrieveSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        queryset =  super().get_queryset().filter(post=post_pk, parent=None)
        return queryset
    
    def get_serializer_class(self):        
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentRetrieveSerializer
    
    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response({
                                                'count':queryset.count(),
                                                'status':status.HTTP_200_OK,
                                                'data':serializer.data, 
                                                })

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response({
                        'count':queryset.count(),
                        'status':status.HTTP_200_OK,
                        'data':serializer.data, 
                        })
    
    def post(self, request, *args, **kwargs):
        post_pk = self.kwargs.get('post_pk')
        serializer = self.get_serializer(data=request.data, context={'post_id': post_pk, 'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


        # return self.create(request, *args, **kwargs)

class CommentRetriveUpdateDeleteApiView(generics.GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    
    def get_serializer_class(self):        
        if self.request.method == 'PATCH':
            return CommentCreateSerializer
        return CommentRetrieveSerializer
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return self.retrieve(request, *args, **kwargs)
    

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return self.update(request, *args, **kwargs)

    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # return self.destroy(request, *args, **kwargs)



class RepliesApiView(mixins.ListModelMixin,
                     generics.GenericAPIView):
    
    queryset = Comment.objects.all()
    serializer_class = RepliesListSerializer

    def get_queryset(self):
        comment_id = self.kwargs.get('pk')
        post_id = self.kwargs.get('post_pk')
        return super().get_queryset().filter(parent=comment_id, post=post_id)
    

        
    def get_permissions(self):
        return super().get_permissions()





def test(request):
    posts = Post.objects.aggregate(Count('title'))
    print(posts)
    
    return HttpResponse("hello world")
