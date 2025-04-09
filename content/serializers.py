from rest_framework import serializers
from .models import ContentVersion

class ContentVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentVersion
        fields = "__all__"
