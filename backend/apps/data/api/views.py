from enum import Enum
from uuid import UUID
from typing import Any
from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from data.models import Profile
from data.api.serializers import *


class ResponseMessages(Enum):
    NO_PROFILE = 'No profile found'
    NO_EXPERIENCE = 'No Experience found'
    NO_EDUCATION = 'No Education'
    USER_DELETED = 'Profile and user deleted'


class ProfileListView(APIView):
    def get(self, request: Request) -> Response:
        profiles: QuerySet = Profile.active_objects.all()
        profiles_data = GetProfileSerializer(profiles, many=True).data
        return Response(data=profiles_data, status=status.HTTP_200_OK)


class ProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def get(self, request: Request, *args: Any, **kwags: Any) -> Request:
        try:
            profile: Profile = request.user.profile
        except ObjectDoesNotExist:
            return Response(data={'error': ResponseMessages.NO_PROFILE.value},
                            status=status.HTTP_404_NOT_FOUND)

        profile_data = GetProfileSerializer(profile).data
        return Response(data=profile_data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        current_user: User = request.user
        has_profile: bool = Profile.objects.filter(user=current_user).exists()
        
        if has_profile:
            instance: Profile = current_user.profile
            serializer = ProfileSerializer(instance, data=request.data)
        else:
            serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=current_user)
            profile_data = GetProfileSerializer(current_user.profile).data
            return Response(data=profile_data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request) -> Response:
        current_user: User = request.user
        current_user.delete()
        return Response(data={'msg': ResponseMessages.USER_DELETED.value},
                        status=status.HTTP_204_NO_CONTENT)


class SingleProfileView(APIView):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        try:
            user = User.objects.get(id=kwargs.get('id'))
            profile_data = GetProfileSerializer(user.profile).data
            return Response(data=profile_data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response(data={'error': ResponseMessages.NO_PROFILE.value},
                            status=status.HTTP_404_NOT_FOUND)


class ExperienceView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request: Request) -> Response:
        current_user: User = request.user
        serializer = ExperienceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(profile=current_user.profile)
            profile_data = GetProfileSerializer(current_user.profile).data
            return Response(data=profile_data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, e_id: UUID) -> Response:
        current_user: User = request.user
        experince: Experience = Experience.active_objects.\
            filter(profile=current_user.profile, id=e_id).first()
        if experince:
            experince.soft_delete() # !
            profile_data = GetProfileSerializer(current_user.profile).data
            return Response(data=profile_data, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': ResponseMessages.NO_EXPERIENCE.value},
                            status=status.HTTP_404_NOT_FOUND)


class EducationView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        current_user: User = request.user
        serializer = EducationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(profile=current_user.profile)
            profile_data = GetProfileSerializer(current_user.profile).data
            return Response(data=profile_data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, e_id: UUID) -> Request:
        current_user: User = request.user
        education: Education = Education.active_objects.\
            filter(profile = current_user.profile, id=e_id).first()
        if education:
            education.soft_delete()
            profile_data = GetProfileSerializer(current_user.profile).data
            return Response(data=profile_data, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': ResponseMessages.NO_EDUCATION.value},
                            status=status.HTTP_404_NOT_FOUND)
