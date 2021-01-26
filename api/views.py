from pprint import pprint
from uuid import UUID

from django.db.models import F
from django.http import HttpResponse, JsonResponse
from quiz.models import Choice, Question, Quiz, QuizAnswer
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (ChoiceSerializer, QuestionChoiceSerializer,
                          QuestionSerializer, QuizAnswerSerializer,
                          QuizDetailSerialize, QuizDictSerializer,
                          QuizSerializer)

@api_view(["GET"])
def index(request):
    api_urls = {
        'List quiz records - Create new quiz: GET': 'quiz/',
        'Get list of questions and answers for test': 'start_quiz/',
        'Submit quiz': 'submit_quiz/',
        'View user quiz result': 'quiz/<uuid:quiz_uuid>/'
    }

    return Response(api_urls)

class QuizList(APIView):
    """
        * GET: List all completed quiz
        * POST: Create new quiz: {"username": <new_username>}
    """
    
    def get(self, request, format=None):
        quizzes = Quiz.objects.filter(start__lt=F('end'))
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDetail(APIView):
    """
        List of a users' test results (questions, options, and their performance on each)
    """
    def get(self, request, quiz_uuid):
        quiz_answers = Quiz.objects.filter(id=quiz_uuid)
        serializer = QuizDetailSerialize(quiz_answers, many=True)        
        return Response(serializer.data)


class TakeQuiz(APIView):
    """
        List all questions and options. for user to take test
    """
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionChoiceSerializer(questions, many=True)
        # pprint(serializer.data.__dict__)
        return Response(serializer.data)


class SubmitQuiz(APIView):
    # def get(self, request):
    #     question = Question.objects.all()
    #     serializer = QuestionChoiceSerializer(question, many=True)
    #     return Response(serializer.data)

    def post(self, request):
        # Sample response
        """
        {
            "quiz_dict_response":{
                "question": [1, 2, 3, 4, 5],
                "option": [6,7,8,9,10],
                "user_uuid": "54bc4ace-032c-41dd-a00c-8f1b23ff2246" 
            }
        }
        """
        serializer = QuizDictSerializer(data=request.data)

        if serializer.is_valid():
            user_uuid = serializer.data['quiz_dict_response']['user_uuid']
            submitted_questions = serializer.data['quiz_dict_response']['question']
            submitted_choice = serializer.data['quiz_dict_response']['option']

            # Check that user_uuis is in UUID format
            try:
                verified_user_uuid = UUID(user_uuid, version=4)
            except ValueError:
                errors = {
                    "error": "The user id is not a valid uuid string. Provide a valid uuid."}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            # Check if user exists
            try:
                quiz = Quiz.objects.get(id=verified_user_uuid)
            except Quiz.DoesNotExist:
                errors = {"error": "User does not exist"}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            # If user_uuid is already in QuizAnswer, user has submitted in the past
            # To prevent multiple submissions
            check_prior_submission = QuizAnswer.objects.filter(quiz_id=verified_user_uuid)
            if (len(check_prior_submission) > 0):
                errors = {
                    "error": "This user has already submitted a quiz"}
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            # Count choices that are true
            score = Choice.objects.filter(
                id__in=submitted_choice).filter(answer=True).count()
            total = len(submitted_questions)

            # Save other quiz parameters
            quiz.score = score
            quiz.total = total
            quiz.save()

            # Store user response
            options = Choice.objects.filter(id__in=submitted_choice)

            # This should come before saving the score, else if there is error we would have saved the score
            for s_question, s_choice in zip(submitted_questions, submitted_choice):
                question = Question.objects.get(id=s_question)
                choice = Choice.objects.get(id=s_choice)

                quiz_answer = QuizAnswer.objects.create(question=question, answer=choice.answer, choice=choice,
                                                     quiz=quiz)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





