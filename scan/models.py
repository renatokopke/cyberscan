from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import JSONField


class ScanReports(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    json_result = JSONField(blank=True, null=True)
    report_path = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.id, self.report_path, self.timestamp)