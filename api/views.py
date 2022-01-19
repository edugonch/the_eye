from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import django_rq
from api.workers import new_event_worker

@api_view(('POST',))
@permission_classes([IsAuthenticated])
def event(request):
    if request.method == 'POST':
        new_event_worker.delay(request.POST)
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
