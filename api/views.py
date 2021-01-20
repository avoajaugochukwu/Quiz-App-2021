from django.http import HttpResponse, JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import TestDetail, Question, Option
from .serializers import TestDetailSerializer, CombinedSerializer


class ResultViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
    """
    queryset = TestDetail.objects.all()
    serializer_class = TestDetailSerializer

class TakeTestViewSet(viewsets.ModelViewSet):
    """
        Show test questions and options
    """
    queryset = Option.objects.all()
    serializer_class = CombinedSerializer
    

    pass
class ResultList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        test_detail = TestDetail.objects.all()
        serializer = TestDetailSerializer(test_detail, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TestDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

