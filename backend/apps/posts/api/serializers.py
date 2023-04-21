from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from posts.models import *


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'text',
            'name',
            'avatar',
            'date',
            'likes',
            'post_comments',
        )
        read_only_fields = ('post_comments',)


class CommentSerializer(ModelSerializer):
    name = serializers.CharField(source='user.name', read_only=True)
    avatar = serializers.URLField(source='user.avatar', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'post',
            'text',
            'date',
            'name',
            'avatar',
        )


class GetPostSerializer(ModelSerializer):
    post_comments = CommentSerializer(many=True)
    
    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'text',
            'name',
            'avatar',
            'date',
            'likes',
            'post_comments',
        )
