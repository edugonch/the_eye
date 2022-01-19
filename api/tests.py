from django.test import TestCase
from rest_framework.test import RequestsClient
from rest_framework import status
import django_rq
from api.models import Event, Session
from api.serializers import EventSerializer
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
DEFAULT_DATE = datetime.strptime('2021-01-01 09:15:27', DATE_FORMAT)

class EventTestCase(TestCase):
    def setUp(self):
        session = Session.objects.create(id='e2085be5-9137-4e4e-80b5-f1ffddc25423')
        Event.objects.create(
            session=session,
            category='page interaction',
            name='cta click',
            data={
                "host": "www.consumeraffairs.com",
                "path": "/",
                "element": "chat bubble"
            },
            time_of_occurrence=DEFAULT_DATE,
        )
        Event.objects.create(
            session=session,
            category='form interaction',
            name='submit',
            data={
                "host": "www.consumeraffairs.com",
                "path": "/",
                "form": {
                    "first_name": "John",
                    "last_name": "Doe"
                },
            },
            time_of_occurrence=DEFAULT_DATE,
        )

    def test_events_attributes(self):

        event1 = Event.objects.get(name="cta click")
        event2 = Event.objects.get(name="submit")
        self.assertEqual(event1.category, 'page interaction')
        self.assertEqual(event1.data['host'], 'www.consumeraffairs.com')
        self.assertEqual(event1.data['path'], '/')
        self.assertEqual(event1.data['element'], 'chat bubble')
        self.assertEqual(event1.time_of_occurrence.replace(tzinfo=None), DEFAULT_DATE)


class EventPostEndpointCase(TestCase):
    rest_client = RequestsClient()
    event_data1 = {
        "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
        "category": "page interaction",
        "name": "pageview",
        "data": {
            "host": "www.consumeraffairs.com",
            "path": "/"
        },
        "time_of_occurrence": "2021-01-01 09:15:27.243860"
    }
    queue = django_rq.get_queue('default')
        

    def test_session_creation_when_not_exists(self):
        self.queue.empty()

        self.assertEqual(Session.objects.count(), 0)
        
        response = self.rest_client.post('http://127.0.0.1:8000/events/', 
            {
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "pageview",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/"
                },
                "time_of_occurrence": "2021-01-01 09:15:27.243860"
            }
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.assertEqual(len(self.queue.jobs), 1)

class EventSerializerCase(TestCase):


    def test_create_new_event(self):
        serializer = EventSerializer(data={
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "pageview",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/"
                },
                "time_of_occurrence": datetime.now()
            }
            
        )

        self.assertEqual(serializer.is_valid(), True)

        serializer.save()

        self.assertEqual(Event.objects.count(), 1)

        self.assertEqual(Session.objects.count(), 1)


    def test_only_one_session_is_created(self):
        serializer1 = EventSerializer(data={
                "session_id": "5555555555555",
                "category": "page interaction1",
                "name": "pageview",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/"
                },
                "time_of_occurrence": datetime.now()
            }
            
        )

        serializer2 = EventSerializer(data={
                "session_id": "5555555555555",
                "category": "page interaction2",
                "name": "pageview",
                "data": {
                    "host": "www.consumeraffairs.com",
                    "path": "/"
                },
                "time_of_occurrence": datetime.now()
            }
            
        )

        serializer1.is_valid()
        serializer1.save()

        serializer2.is_valid()
        serializer2.save()

        self.assertEqual(Session.objects.count(), 1)