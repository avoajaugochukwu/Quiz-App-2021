from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('start_test', views.StartTest.as_view(), name='start_test'),
    path('take_quiz/<uuid:test_uuid>', views.take_quiz, name='take_quiz'),
    path('submit_test', views.submit_test, name='submit_test'),
    path('result_list', views.result_list, name='result_list'),
    path('result_detail/<uuid:test_uuid>', views.result_detail, name='result_detail'),

]
