from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, reverse, get_object_or_404
from .models import *
from .forms import TestDetailForm
from datetime import datetime

# Create your views here.
def index(request):
    form = TestDetailForm()

    title = 'Quiz App - Python Django'

    return render(request, 'quiz/index.html', {'form': form, 'title': title})

def initialize_test(request):
    # We are using a post here because we save the username to the database
    if request.method == 'POST':
        form = TestDetailForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            now = datetime.now()
            ''' Create details for new test
                And obtain the uuid, that will be used to store other parameters
                Like score, response and others '''
            TestDetail.objects.create(start=now, end=now, username=username)

            test_detail = TestDetail.objects.filter(start=now)

            new_uuid = test_detail[0].id
            
            return HttpResponseRedirect(reverse('quiz:take_test', args=(new_uuid,)))

    return render(request, 'quiz/index.html', context)


def take_test(request, test_uuid):

    test_detail = get_object_or_404(TestDetail, pk=test_uuid)

    new_uuid = test_detail.id
    questions = Question.objects.all()
    options = Option.objects.all()
    title = 'Quiz App - Take Test'

    context = {
        'questions': questions,
        'options': options,
        'new_uuid': new_uuid,
        'title': title
    }

    return render(request, 'quiz/take_test.html', context)

def submit_test(request):
    if request.method == 'POST':

        test_uuid = request.POST['test_uuid']
        ''' Obtain post keys and values and convert to list
            post_keys contains the question id
            post_values holds the option id '''
        post_keys = list(request.POST.keys())
        post_values = list(request.POST.values())
        
        ''' Eliminate the first two items in post_keys & post_values
            Because they are the csrf and uuid keys and values
            Then convert remaining values in the lists to integers
            Using list comprehension '''
        list_question_id = [int(i) for i in post_keys[2:]]
        list_option_id = [int(i) for i in post_values[2:]]

        # Get selected option objects from db
        options = Option.objects.filter(id__in=list_option_id)

        # Calculate score and total using selected option objects
        score = 0
        total = len(options)

        for i in options:
            if i.answer == True:
                score += 1

        # Get test_details object, so that test details can be saved
        test_detail = TestDetail.objects.get(id=test_uuid)
        test_detail.score = score
        test_detail.total = total
        test_detail.save()

        ''' Loop through list of questions and list of options from POST request
            and also options object queryset
            So that we can tie all into the Response object,
            which will help to show case results with highlight for wrong and right answers'''
        for i, j, k in zip(list_question_id, list_option_id, options):
            question = Question.objects.get(id=i)
            option = Option.objects.get(id=j)

            response = Response.objects.create(question_id=question, answer=k.answer, option_id=option, test_id=test_detail)

        return HttpResponseRedirect(reverse('quiz:result_details', args=(test_uuid,)))

    return render(request, 'quiz/index.html')


# We would eventually pass the test_id to this view to use it to filter the Response object
# in future only questions and options that have related test id will be passed to the frontend
def result_details(request, test_uuid):
    ''' Prepare objects for result view

           In the next few lines of code, we try to minimize the amount of objects that is sent back to the view
           We exploit the relationships between the Question, Options and Response model to achieve this
           By tying back every object to the test_id of the current user '''
    responses = Response.objects.filter(test_id=test_uuid)

    # Obtain only questions related to the test_id
    response_question_id = [i.question_id.id for i in responses]
    questions = Question.objects.filter(id__in=response_question_id)

    # Obtain only options related to only questions that have been filtered using test_id
    question_options_id = [i.id for i in questions]
    options = Option.objects.filter(question_id__in=question_options_id)


    test_detail = TestDetail.objects.get(id=test_uuid)

    title = 'Quiz App - View your answers'

    context = {
        'questions': questions,
        'options': options,
        'responses': responses,
        'test_detail': test_detail
    }
    
    return render(request, 'quiz/result.html', context)


def result_list(request):
    test_details = TestDetail.objects.all()

    print(test_details)

    context = {
        'test_details': test_details
    }

    return render(request, 'quiz/result_list.html', context)