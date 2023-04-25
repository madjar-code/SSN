from enum import Enum
from uuid import UUID
from typing import (
    Any
)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from posts.models import *
from posts.api.serializers import (
    PostSerializer,
    GetPostSerializer,
    CommentSerializer,
)


class ResponseMessages(str, Enum):
    NO_POST = 'No post found'
    NO_COMMENT = 'No comment found'
    POST_DELETED = 'Post deleted'
    COMMENT_DELETED = 'Comment Deleted'
    UNAUTHORIZED = 'Unauthorized'


class PostView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        post_id: UUID = kwargs.get('id')
        if post_id:
            try:
                post = Post.active_objects.get(id=post_id)
                return Response(GetPostSerializer(post).data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': ResponseMessages.NO_POST.value},
                                status=status.HTTP_404_NOT_FOUND)
        else:
            posts = Post.active_objects.all()
            posts_data = PostSerializer(posts, many=True).data
            return Response(data=posts_data, status=status.HTTP_200_OK)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = PostSerializer(data=request.data)
        current_user: User = request.user

        if serializer.is_valid():
            serializer.save(user=current_user,
                            name=current_user.name,
                            avatar=current_user.avatar)
            return Response(data=serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        post_id: UUID = kwargs.get('id')
        try:
            post: Post = Post.active_objects.get(id=post_id)
            if post.user.id == request.user.id:
                post.soft_delete()
                return Response({'msg': ResponseMessages.POST_DELETED.value},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': ResponseMessages.UNAUTHORIZED.value},
                                status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'error': ResponseMessages.NO_POST.value},
                            status=status.HTTP_404_NOT_FOUND)


class LikeUnlikeView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request,
             *args: Any, **kwargs: Any) -> Response:
        post_id: UUID = kwargs.get('id')
        current_user: User = request.user
        try:
            post: Post = Post.active_objects.get(id=post_id)
            liked: bool = post.likes.filter(id=current_user.id).exists()
            
            if liked:
                post.likes.remove(current_user.id)
            else:
                post.likes.add(current_user.id)
            post.save()
            return Response(GetPostSerializer(post).data,
                            status=status.HTTP_200_OK)
        except:
            return Response({'error': ResponseMessages.NO_POST},
                            status=status.HTTP_404_NOT_FOUND)


class CommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request,
             *args: Any, **kwargs: Any) -> Response:
        post_id: UUID = kwargs.get('id')

        serializer = CommentSerializer(data=request.data)
        
        if serializer.is_valid():
            post: Post = Post.active_objects.filter(id=post_id).first()
            if post:
                serializer.save(user=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': ResponseMessages.NO_POST.value},
                                status=status.HTTP_404_NOT_FOUND)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request,
               *args: Any, **kwargs: Any) -> Response:
        comment_id: UUID = kwargs.get('id')
        try:
            comment: Comment = Comment.active_objects.get(id=comment_id)
            if comment.user.id == request.user.id:
                comment.soft_delete()
                return Response({'msg': ResponseMessages.COMMENT_DELETED.value},
                                status=status.HTTP_200_OK)
            else:
                return Response({'error': ResponseMessages.UNAUTHORIZED.value},
                                status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'error': ResponseMessages.NO_COMMENT.value},
                            status=status.HTTP_404_NOT_FOUND)
