from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        '''user 생성 및 비밀번호 암호화'''
        user = get_user_model().objects.create_user(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        '''user 업데이트'''
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
    

class AuthTokenSerializer(serializers.Serializer):
    '''토큰 serializer'''
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        '''검증 및 인증 이메일로 변경'''
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs