from pprint import pprint
from uuid import UUID

from django.db.models import F
from django.http import HttpResponse, JsonResponse
from quiz.models import Choice, Question, Quiz, QuizAnswer
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (ChoiceSerializer, QuestionChoiceSerializer,
                          QuestionSerializer, QuizAnswerSerializer,
                          QuizDetailSerialize, QuizDictSerializer,
                          QuizSerializer)

# @api_view(["GET"])
# def index(request):
#     api_urls = {
#         'List': 'submit_test/'
#     }
#     return Response(api_urls)


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
    serializer_class = QuestionChoiceSerializer


class SubmitQuiz(APIView):
    def get(self, request):
        question = Question.objects.all()
        serializer = QuestionChoiceSerializer(question, many=True)
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
        serializer = QuizDictSerializer(data=request.data)

        if serializer.is_valid():
            # Check if all questions are answered
            # Cmpute score and total
            print('-----------------------------------------------------------')
            pprint(request.data)
            print('-----------------------------------------------------------')
            submitted_questions = serializer.data['quiz_dict_response']['question']
            submitted_choice = serializer.data['quiz_dict_response']['option']
            user_uuid = serializer.data['quiz_dict_response']['user_uuid']

            # Check if user_id is valid uuid
            try:
                verified_user_uuid = UUID(user_uuid, version=4)
            except ValueError:
                errors = {
                    "error": "The user id is not a valid uuid string. Provide a valid uuid."}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            # Get selected option objects from db
            # Filter submitted_choice in db that have answers as true and count
            score = Choice.objects.filter(
                id__in=submitted_choice).filter(answer=True).count()
            print(score)
            total = len(submitted_questions)

            # Save to response table
            try:
                quiz = Quiz.objects.get(id=verified_user_uuid)
            except Quiz.DoesNotExist:
                errors = {"error": "User does not exist"}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            quiz.score = score
            quiz.total = total
            quiz.save()

            # Store user response
            options = Choice.objects.filter(id__in=submitted_choice)

            # This should come before saving the score, else if there is error we would have saved the score
            for i, j, k in zip(submitted_questions, submitted_choice, options):
                question = Question.objects.get(id=i)
                choice = Choice.objects.get(id=j)

                response = QuizAnswer.objects.create(question=question, answer=k.answer, choice=choice,
                                                     quiz=quiz)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDetail(APIView):
    def get(self, request, quiz_uuid):
        quiz_answers = Quiz.objects.filter(id=quiz_uuid)
        serializer = QuizDetailSerialize(quiz_answers, many=True)        
        return Response(serializer.data)


class QuizList(ListAPIView):
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.filter(start__lt=F('end'))
