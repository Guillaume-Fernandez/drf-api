from rest_framework import filters

from common.views import CommonBaseViewSet

from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(CommonBaseViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'name']
    ordering = ['-id']