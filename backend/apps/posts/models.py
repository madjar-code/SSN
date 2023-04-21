from django.db import models
from common.mixins.models import BaseModel
from common.fields import OptionalCharField
from users.models import User


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts', blank=True)
    text = models.CharField(max_length=255)
    name = OptionalCharField()
    avatar = models.URLField(max_length=200, blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text

    class Meta:
        ordering = ('-date',)


class Comment(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='user_comments', blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        related_name='post_comments', blank=True)
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.text} - {self.user.name}'

    class Meta:
        ordering = ('-date',)