from django.urls import path

from api import views

urlpatterns = [
    path('solve', views.WPMSSolverView),
]
