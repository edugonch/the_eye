from api.models import Session, Event
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from api.serializers import SessionSerializer, EventSerializer

class EventView(CreateAPIView):
    """
    View for that only create events
    """
    serializer_class = EventSerializer
