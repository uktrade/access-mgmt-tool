from django.db import models
from django.utils.module_loading import import_string


class Integration(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255, help_text="The dotted path to the ingregration class")

    def get_object(self):
        return import_string(self.path)(self)

    def __str__(self):
        return self.name


class Application(models.Model):
    integration = models.ForeignKey(Integration, on_delete=models.CASCADE)
    name = models.SlugField()
    description = models.TextField()
    configuration = models.JSONField(null=True, blank=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
