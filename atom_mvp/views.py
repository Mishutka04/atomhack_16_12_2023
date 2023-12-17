from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transformers import pipeline
import torch

from .serializers import GenerateAnswerSerializer


class GenerateAnswerView(APIView):
    
    serializer_class = GenerateAnswerSerializer

    model = "Denis431/docs_generate_v2"
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipe = pipeline(
        "text-generation",
        model=model,
        device=device
        )

    def post(self, request):
        serializer = GenerateAnswerSerializer(
            data=request.data)

        if serializer.is_valid():
            input_text = serializer.validated_data['input_text']
            try:
                generated_text = self.pipe(
                    input_text, max_length=100,
                    num_return_sequences=1)[0]['generated_text']
                return Response(
                    {'generated_text': generated_text},
                    status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(
                {'error': 'Invalid input data'},
                status=status.HTTP_400_BAD_REQUEST)
