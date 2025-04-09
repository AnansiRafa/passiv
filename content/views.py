from rest_framework import viewsets
from .models import ContentVersion
from .serializers import ContentVersionSerializer

class ContentVersionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentVersion.objects.order_by("-timestamp")
    serializer_class = ContentVersionSerializer
