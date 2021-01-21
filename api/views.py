from pprint import pprint

from django.http import HttpResponse, JsonResponse
from quiz.models import Choice, Question, Quiz, QuizAnswer
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (ChoiceSerializer, QuestionSerializer,
                          SubmitQuizSerializer, QuizSerializer)


class ResultViewSet(viewsets.ModelViewSet):
    """
        Get: View all test attempts
        Add: Create new user
    """
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class TakeTestViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class SubmitTest(APIView):
    def get(self, request):
        quiz = Question.objects.all()
        serializer = QuestionSerializer(quiz, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Sample response
        """
        {
            "response":{
                "question": [1, 2, 3, 4, 5],
                "option": [6,7,8,9,10],
                "user_uuid": "54bc4ace-032c-41dd-a00c-8f1b23ff2246" 
            }
        }
        """
        """
            question: [1, 2, 3, 4, 5]
            answer: [3, 6, 9, 16, 17]
            answer_interpret: [n, y, y, n, y]
            score: 3/5
        """
        serializer = SubmitQuizSerializer(data=request.data)

        if serializer.is_valid():
            # Check if all questions are answered
            # Cmpute score and total
            print('-----------------------------------------------------------')
            submitted_questions = serializer.data['quiz_response']['question']
            submitted_options = serializer.data['quiz_response']['option']
            user_uuid = serializer.data['quiz_response']['user_uuid']

            # Get selected option objects from db
            # Filter submitted_options in db that have answers as true and count
            score = Option.objects.filter(
                id__in=submitted_options).filter(answer=True).count()
            print(score)
            total = len(submitted_questions)
            # Save to response table

            try:
                quiz = Quiz.objects.get(id=user_uuid)
                quiz.score = score
                quiz.total = total
                quiz.save()
            except TestDetail.DoesNotExist:
                errors = {"error": "User does not exist"}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            # Store user response
            options = Option.objects.filter(id__in=submitted_options)

            for i, j, k in zip(submitted_questions, submitted_options, options):
                question = Question.objects.get(id=i)
                option = Option.objects.get(id=j)

                response = Response.objects.create(question_id=question, answer=k.answer, option_id=option,
                                               test_id=quiz)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
