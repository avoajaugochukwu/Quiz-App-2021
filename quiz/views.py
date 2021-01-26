from django.contrib import messages
from django.db import IntegrityError
from django.db.models import F
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.views.generic.list import ListView


from .forms import QuizForm
from .models import Choice, Question, Quiz, QuizAnswer


class Index(View):
    def get(self, request):
        form = QuizForm()

        return render(request, 'quiz/index.html', {'form': form})


class StartTest(View):
    # Initialize new test details, and redirect to test page
    def get(self, request):
        form = QuizForm()
        return render(request, 'quiz/index.html', {'form': form})

    def post(self, request):
        form = QuizForm(request.POST)

        if form.is_valid():
            new_quiz = form.save()
            # Session will be used to track if users answered all the questions
            request.session['unanswered_questions'] = False

            return HttpResponseRedirect(reverse('quiz:quiz-take-quiz', args=(new_quiz.id,)))

        return render(request, 'quiz/index.html', {'form': form})


def take_quiz(request, test_uuid):
    quiz = get_object_or_404(Quiz, pk=test_uuid)

    new_uuid = quiz.id
    questions = Question.objects.all()
    choices = Choice.objects.all()
    title = 'Quiz App - Take a shot'

    
    # unanswered_question will be false for new test
    # If this view is called from submit_test due to unanswered questions
    # Then unanswered_questions will be true, trigerring an alert in the template
    unanswered_questions = request.session['unanswered_questions']
    print(choices)
    context = {
        'questions': questions,
        'choices': choices,
        'new_uuid': new_uuid,
        'title': title,
        'unanswered_questions': request.session['unanswered_questions']
    }

    return render(request, 'quiz/take_quiz.html', context)


def submit_test(request):
    if request.method == 'POST':

        test_uuid = request.POST['test_uuid']

        # questions_count is used to track number of questions in the quiz
        # We would use it to compare result
        # To know when users didn't finish the test
        questions_count = request.POST['questions_count']

        # Obtain post keys and values and convert to list
        # post_keys contains the question id
        # post_values holds the option id
        post_keys = list(request.POST.keys())
        post_values = list(request.POST.values())

        # Eliminate the first three items in post_keys & post_values
        # Because they are for the csrf, uuid keys and questions_count and values
        # Then convert remaining items in the lists to integers
        # Using list comprehension
        list_question_id = [int(i) for i in post_keys[3:]]
        list_option_id = [int(i) for i in post_values[3:]]
        print(list_question_id, list_option_id)
        # Compare total questions count to number of options submitted
        if int(questions_count) > len(list_option_id):
            request.session['unanswered_questions'] = True
            return HttpResponseRedirect(reverse('quiz:quiz-take-quiz', args=(test_uuid,)))

        # Get selected option objects from db
        choices = Choice.objects.filter(id__in=list_option_id)

        # Calculate score and total using selected option objects
        score = 0
        total = len(choices)

        for i in choices:
            if i.answer == True:
                score += 1

        # Get quiz object, so that test details can be saved
        quiz = Quiz.objects.get(id=test_uuid)
        quiz.score = score
        quiz.total = total
        quiz.save()

        # Loop through list of questions and list of choices from POST request
        # and also choices object queryset
        # So that we can tie all into the Response object,
        # which will help to show case results with highlight for wrong and right answers
        for i, j, k in zip(list_question_id, list_option_id, choices):
            question = Question.objects.get(id=i)
            choice = Choice.objects.get(id=j)

            QuizAnswer.objects.create(question=question, answer=k.answer, choice=choice,
                                               quiz=quiz)

        return HttpResponseRedirect(reverse('quiz:quiz-result-detail', args=(test_uuid,)))

    return render(request, 'quiz/index.html')


# We would eventually pass the quiz_id to this view to use it to filter the Response object
# in future only questions and options that have related test id will be passed to the frontend
def result_detail(request, test_uuid):
    # Prepare objects for result view

    # In the next few lines of code, we try to minimize the amount of objects that is sent back to the view
    # We exploit the relationships between the Question, Options and Response model to achieve this
    # By tying back every object to the quiz_id of the current user
    quiz_answers = QuizAnswer.objects.filter(quiz_id=test_uuid)

    # Obtain only questions related to the quiz_id
    quiz_answers_question_ids = [i.question.id for i in quiz_answers]
    questions = Question.objects.filter(id__in=quiz_answers_question_ids)

    # Obtain only options related to only questions that have been filtered using quiz_id
    question_choice_ids = [i.id for i in questions]
    choices = Choice.objects.filter(question_id__in=question_choice_ids)

    quiz = Quiz.objects.get(id=test_uuid)

    title = 'Quiz App - View your answers'

    context = {
        'questions': questions,
        'choices': choices,
        'quiz_answers': quiz_answers,
        'quiz': quiz,
        'title': title
    }

    return render(request, 'quiz/result_detail.html', context)


def result_list(request):
    # This filter uses the Django F expression to compare two fields in the same model
    # Here we are comparing the test start and end time, which were initialized with the
    # same value.

    # If the test was completed then the end time will be updated at submission.

    # If they are the same, it means the user did not finish the test,
    # because end time is updated when test is completed and submitted.

    # start__lt=F('end') means: start field is less than end field

    
    quizzes = Quiz.objects.filter(start__lt=F('end'))

    title = 'Quiz App - View all results'

    context = {
        'quizzes': quizzes,
        'title': title
    }

    return render(request, 'quiz/result_list.html', context)
