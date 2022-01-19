from api.models import Session, Event
from django.db import transaction
from rest_framework import serializers

class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'created_at', 'updated_at']

class EventSerializer(serializers.HyperlinkedModelSerializer):

    session_id = serializers.CharField(write_only=True, max_length=250)

    def create(self, validated_data):
        with transaction.atomic():
            session_id = validated_data.get('session_id')
            session = Session.objects.get_or_create(id=session_id)

            event = Event()
            event.session = session[0]
            event.category = validated_data.get('category')
            event.name = validated_data.get('name')
            event.data = validated_data.get('data')
            event.time_of_occurrence = validated_data.get('time_of_occurrence')
            
            event.save()
            return event

    class Meta:
        model = Event
        fields = ['session_id', 'category', 'name', 'data', 'time_of_occurrence']
        extra_kwargs = {
            'session_id': {'write_only': True}
        }