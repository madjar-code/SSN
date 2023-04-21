from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from common.utils import get_gravatar
from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'avatar',
            'date',
            'password',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True
            }
        }

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)
        user.avatar = get_gravatar(validated_data.get('email'))
        user.save()
        Token.objects.create(user=user)
        return user