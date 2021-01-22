from django.urls import include, path
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'results', views.ResultViewSet)
router.register(r'take_test', views.TakeTestViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('submit_quiz/', views.SubmitQuiz.as_view()),
    path('result/', views.ResultList.as_view()),
    path('result/<uuid:quiz_uuid>', views.ResultDetail.as_view()),
]