import json
import sys

from rest_framework.generics import RetrieveAPIView, CreateAPIView
from serathonapp import serializers
from django.shortcuts import render
import requests
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

tradesoft_token = "vMWKBzqi-lBFy-VhCF-qNXr"
owner = "100421-100"
oneriver_token = "723ea96a9baec692c5d1ffde6f3a90f0ea0798180b895ed2d828a4cf97ad47f0"

sys.path.append('core/nlp_base')
sys.path.append('core/keyword_extraction/src')
import nlp_api

nlp_engine = nlp_api.NlpBase()

class EmirGiris(CreateAPIView):

    serializer_class = serializers.EmirGirisSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        headers = {'Content-type': 'application/json'}
        url = "https://ts.tradesoft.com.tr/Serathonin/EQ/addOrder"
        data_cre = dict(token=tradesoft_token, tradesoft_token=owner, accountExtId=owner,
                         finInst=data["finInst"], orderDate=data["orderDate"],
                         orderType=data["orderType"], orderTimeInForce=data["orderTimeInForce"],
                         orderUnits=data["orderUnits"], orderPrice=data["orderPrice"],
                         buySell=data["buySell"], shortFall=data["shortFall"], checkOnly=data["checkOnly"],
                         maxFloor=data["maxFloor"])

        response = requests.request(
            "POST", url, data=json.dumps(data_cre), headers=headers)

        return Response(response.content)


class EmirIzle(CreateAPIView):

    serializer_class = serializers.EmirIzleSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        print(nlp_engine.lemmatize_all("öldürdüm,perde"))

        headers = {'Content-type': 'application/json'}
        url = "https://ts.tradesoft.com.tr/Serathonin/EQ/getOrders"
        data_cre = dict(token=tradesoft_token, tokenOwner=owner, accountExtId=owner,
                        transactionId=data["transactionId"])

        response = requests.request(
            "POST", url, data=json.dumps(data_cre), headers=headers)

        return Response(json.loads(response.content))


class KiymetDagilim(CreateAPIView):
    serializer_class = serializers.OneriverSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        headers = {'Content-type': 'application/json', 'X-Client-Token': oneriver_token}
        url = "https://robodemo.infina.com.tr/robo/api/v0.7L/distribution"
        data = dict(start_amount=data["start_amount"], monthly_amount=data["monthly_amount"],
                        age=data["age"], risk=data["risk"])

        response = requests.request(
            "POST", url, data=json.dumps(data), headers=headers)

        return Response(json.loads(response.content))


class TahminiGetiri(CreateAPIView):

    serializer_class = serializers.OneriverSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        headers = {'Content-type': 'application/json', 'X-Client-Token': oneriver_token}
        url = "https://robodemo.infina.com.tr/robo/api/v0.7L/return"
        data = dict(start_amount=data["start_amount"], monthly_amount=data["monthly_amount"],
                    age=data["age"], risk=data["risk"])

        response = requests.request(
            "POST", url, data=json.dumps(data), headers=headers)

        return Response(json.loads(response.content))
