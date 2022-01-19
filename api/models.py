from django.db import models

class Session(models.Model):
    id = models.CharField(primary_key=True, max_length=250, unique=True, default=id)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Event(models.Model):
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    data = models.JSONField("data", default={})
    time_of_occurrence = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ErrorLog(models.Model):
    session_id = models.CharField(max_length=250, blank=True, default='')
    event_payload = models.TextField()
    error_message = models.TextField()
    place_of_error = models.CharField(max_length=250, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)