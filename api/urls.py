from django.urls import include, path
from . import views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'results', views.ResultViewSet)
router.register(r'take_test', views.TakeTestViewSet)

urlpatterns = [
    # path('', views.index, name='api-index'),
    path('', include(router.urls)),
    # path('test/', views.ResultListViewSet, name='api-one'),
    path('open/', views.ResultList.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)