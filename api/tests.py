import json
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import RequestsClient
from rest_framework import status
import django_rq
from api.models import Event, Session
from api.serializers import EventSerializer, PageViewEventSerializer, CtaClickEventSerializer, FormInteractionEventSerializer
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
                "host": "https://www.consumeraffairs.com",
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
                "host": "https://www.consumeraffairs.com",
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
        self.assertEqual(event1.data['host'], 'https://www.consumeraffairs.com')
        self.assertEqual(event1.data['path'], '/')
        self.assertEqual(event1.data['element'], 'chat bubble')
        self.assertEqual(event1.time_of_occurrence.replace(tzinfo=None), DEFAULT_DATE)


class EventPostEndpointCase(TestCase):
    def setUp(self):
        # Create User
        user = User.objects.create(email='test@test.com', username='example.com')
        # Create token
        Token.objects.create(user=user)


    rest_client = RequestsClient()
    event_data1 = {
        "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
        "category": "page interaction",
        "name": "pageview",
        "data": {
            "host": "https://www.consumeraffairs.com",
            "path": "/"
        },
        "time_of_occurrence": "2021-01-01 09:15:27.243860"
    }
    queue = django_rq.get_queue('default')

    def test_unauthorized_request(self):
        response = self.rest_client.post('http://127.0.0.1:8000/events/', 
            json.dumps ({
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "pageview",
                "data": {
                    "host": "https://www.consumeraffairs.com",
                    "path": "/"
                },
                "time_of_occurrence": "2021-01-01 09:15:27.243860"
            })
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                

    def test_session_creation_when_not_exists(self):
        self.queue.empty()

        self.assertEqual(Session.objects.count(), 0)
        
        response = self.rest_client.post('http://127.0.0.1:8000/events/', 
            json.dumps ({
                "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
                "category": "page interaction",
                "name": "pageview",
                "data": {
                    "host": "https://www.consumeraffairs.com",
                    "path": "/"
                },
                "time_of_occurrence": "2021-01-01 09:15:27.243860"
            }), headers={'Authorization': 'Token {}'.format(Token.objects.last())}
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
                    "host": "https://www.consumeraffairs.com",
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
                    "host": "https://www.consumeraffairs.com",
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
                    "host": "https://www.consumeraffairs.com",
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


class PageViewEventSerializerCase(TestCase):
    def test_wrong_host_url(self):
        serializer = PageViewEventSerializer(data={
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "page interaction",
            "name": "pageview",
            "data": {
                "host": "not an url",
                "path": "/",
            },
            "time_of_occurrence": datetime.now()
            }
        )

        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(serializer.errors['data'][0].title(), "Host Is Not In The Correct Format Not An Url.")

    def test_wrong_path(self):
        serializer = PageViewEventSerializer(data={
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "page interaction",
            "name": "pageview",
            "data": {
                "host": "https://www.consumeraffairs.com",
                "path": "this is not a path",
            },
            "time_of_occurrence": datetime.now()
            }
        )

        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(serializer.errors['data'][0].title(), "Path Is Not In The Correct Format This Is Not A Path")

class CtaClickEventSerializerCase(TestCase):
    def test_element_not_present(self):
        serializer = CtaClickEventSerializer(data={
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "page interaction",
            "name": "cta click",
            "data": {
                "host": "https://www.consumeraffairs.com",
                "path": "/",
            },
            "time_of_occurrence": datetime.now()
            }
        )

        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(serializer.errors['data'][0].title(), "Missing Element Keyworkd On Payload {'Host': 'Https://Www.Consumeraffairs.Com', 'Path': '/'}")

class FormInteractionEventSerializerCase(TestCase):
    def test_form_incorrect_format(self):
        serializer = FormInteractionEventSerializer(data={
            "session_id": "e2085be5-9137-4e4e-80b5-f1ffddc25423",
            "category": "form interaction",
            "name": "submit",
            "data": {
                "host": "https://www.consumeraffairs.com",
                "path": "/",
                "form": "Not a form"
            },
            "time_of_occurrence": datetime.now()
            }
        )

        self.assertEqual(serializer.is_valid(), False)

        self.assertEqual(serializer.errors['data'][0].title(), "Form Is Not In The Correct Format Not A Form")