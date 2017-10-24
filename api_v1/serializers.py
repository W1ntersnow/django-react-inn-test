from rest_framework import serializers
from testapp.models import User


class UserSerializer(serializers.ModelSerializer):
    inn = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'inn',
            'cash',
        ]
