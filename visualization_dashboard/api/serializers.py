from rest_framework import serializers
from .models import DataPoint

class DataPointSerializer(serializers.ModelSerializer):
    end_year = serializers.IntegerField(allow_null=True)
    intensity = serializers.IntegerField(allow_null=True)
    likelihood = serializers.IntegerField(allow_null=True)
    relevance = serializers.IntegerField(allow_null=True)
    start_year = serializers.IntegerField(allow_null=True)

    class Meta:
        model = DataPoint
        fields = '__all__'
