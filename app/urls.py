from django.urls import path
from . import views


urlpatterns = [
  path('stageone', views.stageone),
]