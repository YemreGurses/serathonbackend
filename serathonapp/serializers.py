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


class EmirGirisSerializer(serializers.Serializer):
    finInst = serializers.CharField(required=True)
    orderDate = serializers.CharField(required=True)
    orderType = serializers.IntegerField(required=True)
    orderTimeInForce = serializers.CharField(required=True)
    orderUnits = serializers.IntegerField(required=True)
    orderPrice = serializers.FloatField(required=True)
    buySell = serializers.CharField(required=True)
    shortFall = serializers.IntegerField(required=True)
    checkOnly = serializers.IntegerField(required=True)
    maxFloor = serializers.IntegerField(required=True)


class EmirIzleSerializer(serializers.Serializer):
    transactionId = serializers.CharField(required=True)


class OneriverSerializer(serializers.Serializer):
    start_amount = serializers.CharField(required=True)
    monthly_amount = serializers.CharField(required=True)
    age = serializers.IntegerField(required=True)
    risk = serializers.CharField(required=True)


class UpdateSerializer(serializers.Serializer):
    completed = serializers.BooleanField(required=True)
