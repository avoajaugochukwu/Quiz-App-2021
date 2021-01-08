from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('test', views.test, name = 'test'),
    path('submit_test', views.submit_test, name = 'submit_test'),
    path('result_list', views.result_list, name = 'result_list'),
    path('result_details/<uuid:test_uuid>', views.result_details, name = 'result_details'),
    
]