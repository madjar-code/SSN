from django.urls import path


from .views import *


urlpatterns = [
    path('posts', PostView.as_view()),
    path('posts/<str:id>', PostView.as_view()),
    path('posts/<str:id>/like', LikeUnlikeView.as_view()),
    path('posts/<str:id>/comments', CommentView.as_view()),
    path('posts/comments/<int:id>', CommentView.as_view()),
]
