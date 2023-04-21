from rest_framework.serializers import ModelSerializer
from users.api.serializers import UserSerializer
from data.models import (
    Profile,
    Experience,
    Education,
)


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        # read_only_fields = fields


class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'
        # read_only_fields = fields


class EducationSerializer(ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        # read_only_fields = fields


class GetProfileSerializer(ModelSerializer):
    user = UserSerializer
    experience = ExperienceSerializer(many=True)
    education = EducationSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            'id',
            'user',
            'company',
            'website',
            'location',
            'status',
            'skills',
            'bio',
            'github_username',
            'youtube',
            'twitter',
            'facebook',
            'linkedin',
            'instagram',
            'experience',
            'education',
        )