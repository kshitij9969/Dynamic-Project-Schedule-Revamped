from django.urls import path, include

from . import views

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('project-schedule', views.ProjectScheduleApiSet, basename='project-schedule')

urlpatterns = [
    path('project-detail/', views.ProjectScheduleApiSet.as_view(), name='project-detail'),
    path('project-schedule/', views.ManageProjectDetailsView.as_view(), name='project-schedule')
]
