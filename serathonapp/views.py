import json

from django.shortcuts import render
import requests
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response

token = "vMWKBzqi-lBFy-VhCF-qNXr"
owner = "100421-100"


class EmirGiris(APIView):
    def post(self, request):
        data = request.data
        headers = {'Content-type': 'application/json'}
        url = "https://ts.tradesoft.com.tr/Serathonin/EQ/addOrder"
        data_cre = dict(token=token, tokenOwner=owner, accountExtId=owner,
                         finInst=data["finInst"], orderDate=data["orderDate"],
                         orderType=data["orderType"], orderTimeInForce=data["orderTimeInForce"],
                         orderUnits=data["orderUnits"], orderPrice=data["orderPrice"],
                         buySell=data["buySell"], shortFall=data["shortFall"], checkOnly=data["checkOnly"],
                         maxFloor=data["maxFloor"])

        response = requests.request(
            "POST", url, data=json.dumps(data_cre), headers=headers)

        return Response(response.content)


class EmirIzle(APIView):
    def get(self, request):
        data = request.data
        headers = {'Content-type': 'application/json'}
        url = "https://ts.tradesoft.com.tr/Serathonin/EQ/getOrders"
        data_cre = dict(token=token, tokenOwner=owner, accountExtId=owner,
                        transactionId=data["transactionId"])

        response = requests.request(
            "POST", url, data=json.dumps(data_cre), headers=headers)

        return Response(json.loads(response.content))


