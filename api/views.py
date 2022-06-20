from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


from application.models import Application


class ListApplications(ListAPIView):
    def get(self, request, format=None):
        applications = [(app.name, app.description) for app in Application.objects.filter(active=True)]
        return Response(applications)


class ListApplicationPermissions(ListAPIView):
    def get(self, request, application_name, format=None):
        app = Application.objects.get(name=application_name)

        client = app.integration.get_object()
        permissions = client.list_permissions()

        return Response(permissions)


class CreateAccessRequest(CreateAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
