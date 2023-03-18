from rest_framework import serializers

from common.serializers import CommonHyperlinkedRelatedField
from .models import Task

class TaskSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = CommonHyperlinkedRelatedField
    
    class Meta:
        model = Task
        fields = '__all__'