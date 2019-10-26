import json
import sys

import requests
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ChatterBotCorpusTrainer
from django.http import JsonResponse

from django.views.generic.base import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from serathonapp import serializers
from serathonapp.train import chatbot
from textblob import TextBlob


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

        print(nlp_engine.lemmatize_all("yatırımlarım,önerebilir,eğitim,hisseler"))

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


class UpdatePoint(UpdateAPIView):
    serializer_class = serializers.UpdateSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = request.user
        if data["completed"]:
            user += 10
            user.save(update_fields=["point"])
            return Response({"user": request.user.id, "point": user.point, "detail": "success"},
                            status=status.HTTP_200_OK)
        else:
            return Response({"user": request.user.id, "point": user.point, "detail": "failure"},
                            status=status.HTTP_304_NOT_MODIFIED)


class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(APIView):
    """
    Provide an API endpoint to interact with Chat Assistant.
    """
    # chatterbotex = ChatBot(**settings.CHATTERBOT)
    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.
        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        input_data = TextBlob(input_data['text']).translate(to="en")
        response = chatbot.get_response(str(input_data))
        answer = TextBlob(str(response)).translate(to="tr")
        response_data = {'response': str(answer)}

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': 'Servet Assistant'
        })


class ChatTrain(APIView):

    def post(self, request, *args, **kwargs):
        chatterbotex = ChatBot(**settings.CHATTERBOT)
        trainer = ChatterBotCorpusTrainer(chatterbotex)
        trainer.train("chatterbot.corpus.english")
        return Response({"detail": "success"}, status=status.HTTP_200_OK)

