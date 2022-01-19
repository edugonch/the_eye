from django.db import models

class Session(models.Model):
    id = models.CharField(primary_key=True, max_length=250, unique=True, default=id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Event(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    category = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    data = models.JSONField("data", default={})
    time_of_occurrence = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)