from django.urls import include, path
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'results', views.ResultViewSet)
router.register(r'take_test', views.TakeTestViewSet)



urlpatterns = [
    # path('', include(router.urls)),
    path('', views.index),
    # path('quiz/', views.ResultViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('submit_quiz/', views.SubmitQuiz.as_view()),
    path('quiz/', views.QuizList.as_view()),
    path('quiz/create/', views.QuizDetail.as_view()),
    path('quiz/<uuid:quiz_uuid>', views.QuizDetail.as_view()),
]