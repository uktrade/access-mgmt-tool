from django.db import models

from application.models import Application

class AccessRequest(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    permissions = models.JSONField(null=True, blank=True)
    revoke_access = models.BooleanField(default=False)
    user_id = models.CharField(max_length=255)

    authorised = models.BooleanField(default=False)
    authorised_by = models.ForeignKey("auth.User", null=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.application.name} / {self.user_id}"
