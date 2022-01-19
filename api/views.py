import json
from rest_framework import status
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.workers import new_event_worker
from api.models import ErrorLog

@api_view(('POST',))
@permission_classes([IsAuthenticated])
def event(request):
    if request.method == 'POST':
        try:
            json_body = json.loads(request.body)
            new_event_worker.delay(json_body)
            return Response(status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            with transaction.atomic():
                ErrorLog.objects.create(
                    session = '',
                    event_payload = request.body,
                    error_message=e,
                    place_of_error="event view"
                )
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
