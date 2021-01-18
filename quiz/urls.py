from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.Index.as_view(), name = 'index'),
    path('initialize_test', views.initialize_test, name='initialize_test'),
    path('take_test/<uuid:test_uuid>', views.take_test, name = 'take_test'),
    path('submit_test', views.submit_test, name = 'submit_test'),
    path('result_list', views.result_list, name = 'result_list'),
    path('result_details/<uuid:test_uuid>', views.result_details, name = 'result_details'),
    
]