from django.urls import path

from .views import ListApplications, ListApplicationPermissions

app_name = "api"

urlpatterns = [
    path("application/", ListApplications.as_view()),
    path("application/<str:application_name>/", ListApplicationPermissions.as_view()),
    path("application/<str:application_name>/", ListApplicationPermissions.as_view()),
    path("application/<str:application_name>/", ListApplicationPermissions.as_view()),
]
