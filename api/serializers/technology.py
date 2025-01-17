from rest_framework import serializers

from ..models import Technology


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = "__all__"


class TechnologySerializerUpdate(serializers.Serializer):
    technology_id = serializers.IntegerField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=False)
