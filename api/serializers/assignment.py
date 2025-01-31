from rest_framework import serializers

from ..models.assignment import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"


class AssignmentSerializerCreate(serializers.Serializer):
    project_id = serializers.IntegerField(write_only=True, required=True)
    developer_id = serializers.IntegerField(required=False)
    hours = assignment_id = serializers.IntegerField(required=False)


class AssignmentSerializerUpdate(serializers.Serializer):
    assignment_id = serializers.IntegerField(write_only=True, required=False)
    project_id = serializers.IntegerField(write_only=True, required=False)
    developer_id = serializers.IntegerField(required=False)
    hours = assignment_id = serializers.IntegerField(required=False)
