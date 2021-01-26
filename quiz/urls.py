from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.Index.as_view(), name='quiz-index'),
    path('start_test', views.StartTest.as_view(), name='quiz-start-test'),
    path('take_quiz/<uuid:test_uuid>', views.take_quiz, name='quiz-take-quiz'),
    path('submit_test', views.submit_test, name='quiz-submit-test'),
    path('result_list', views.result_list, name='quiz-result-list'),
    path('result_detail/<uuid:test_uuid>', views.result_detail, name='quiz-result-detail'),

]
