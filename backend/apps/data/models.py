from django.db import models
from common.mixins.models import BaseModel
from common.fields import OptionalCharField
from users.models import User


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='profile', blank=True)
    company = OptionalCharField()
    website = models.URLField(max_length=255, blank=True)
    location = OptionalCharField()
    status = models.CharField(max_length=100)
    skills = models.TextField(help_text='Comma Separated value')
    bio = models.TextField()
    github_username = models.CharField(max_length=50, blank=True)
    youtube = OptionalCharField()
    twitter = OptionalCharField()
    facebook = OptionalCharField()
    linked_in = OptionalCharField()
    instagram = OptionalCharField()
    
    def __str__(self) -> str:
        return self.user.name


class Experience(BaseModel):
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE,
        related_name='experience', blank=True)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title


class Education(BaseModel):
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE,
        related_name='education', blank=True)
    school = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    from_date = models.DateField()
    to_date = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self) -> str:
        return self.school
