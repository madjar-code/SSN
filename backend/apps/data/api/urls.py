from django.urls import path

from .views import *


urlpatterns = [
    path('profile', ProfileView.as_view()),
    path('profiles', ProfileListView.as_view()),
    path('profile/me', ProfileView.as_view()),
    path('profile/experience', ExperienceView.as_view()),
    path('profile/experience/<int:e_id>', ExperienceView.as_view()),
    path('profile/education', EducationView.as_view()),
    path('profile/education/<str:e_id>', EducationView.as_view()),
    path('profile/<str:id>', SingleProfileView.as_view()),
]