from rest_framework import serializers


class TopCustomersSerializer(serializers.Serializer):

    username = serializers.CharField()
    spent_money = serializers.IntegerField()
    gems = serializers.ListField(child=serializers.CharField())
