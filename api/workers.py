from django_rq import job
from django.db import transaction
from api.serializers import PageViewEventSerializer, CtaClickEventSerializer, FormInteractionEventSerializer
from api.models import ErrorLog

@job('default')
def new_event_worker(params):
    is_multiple = isinstance(params, list)

    with transaction.atomic():
        if params["name"] and params["name"] == "pageview":
            serializer = PageViewEventSerializer(data=params, many=is_multiple)
        elif params["name"] and params["name"] == "cta click":
            serializer = CtaClickEventSerializer(data=params, many=is_multiple)
        elif params["name"] and params["name"] == "submit":
            serializer = FormInteractionEventSerializer(data=params, many=is_multiple)
        else:
            ErrorLog.objects.create(
                session_id = '',
                event_payload = params,
                error_message=f"Wrong name interacion keyword found {params['name']}",
                place_of_error="new_event_worker"
            )
            return False

        if serializer.is_valid():
            serializer.save()
        else:
            if is_multiple:
                session= params["session_id"]
            else:
                session_id = ''
            ErrorLog.objects.create(
                session_id = session_id,
                event_payload = params,
                error_message=serializer.errors,
                place_of_error="new_event_worker"
            )