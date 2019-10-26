from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer


class UserSerializer(UserDetailsSerializer):
    salary = serializers.CharField(source='profile.salary')
    married = serializers.CharField(source='profile.married')
    age = serializers.CharField(source='profile.age')
    education = serializers.CharField(source='profile.education')
    risk_level = serializers.IntegerField(source='profile.risk_level')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('salary',
                                                      'married',
                                                      'age',
                                                      'education',
                                                      'risk_level')