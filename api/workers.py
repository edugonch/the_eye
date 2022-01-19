from django_rq import job
from django.db import transaction
from api.serializers import EventSerializer
from api.models import ErrorLog

@job('default')
def new_event_worker(params):
    is_multiple = isinstance(params, list)

    with transaction.atomic():
        serializer = EventSerializer(data=params, many=is_multiple)
        if serializer.is_valid():
            serializer.save()
        else:
            if is_multiple:
                session= params["session_id"]
            else:
                session_id = None
            ErrorLog.objects.create(
                session = session_id,
                event_payload = params,
                error_message=serializer.errors,
                place_of_error="new_event_worker"
        )