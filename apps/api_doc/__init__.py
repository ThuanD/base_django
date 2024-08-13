from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.CharField()


class ValidationErrorSerializer(serializers.Serializer):
    code = serializers.CharField()
    message = serializers.DictField()
