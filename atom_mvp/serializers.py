from rest_framework import serializers


class GenerateAnswerSerializer(serializers.Serializer):
    input_text = serializers.CharField(
        style={'base_template': 'textarea.html'}
    )
