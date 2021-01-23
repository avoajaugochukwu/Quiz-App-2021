from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'api'

router = routers.DefaultRouter()
# router.register(r'results', views.ResultViewSet)
# router.register(r'take_test', views.TakeTestViewSet)



urlpatterns = [
    # path('', include(router.urls)),
    path('', views.index),
    # path('quiz/', views.ResultViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('quiz/', views.QuizList.as_view()),
    path('take_quiz/', views.TakeQuiz.as_view()),
    path('submit_quiz/', views.SubmitQuiz.as_view()),
    path('quiz/<uuid:quiz_uuid>', views.QuizDetail.as_view()),
]
