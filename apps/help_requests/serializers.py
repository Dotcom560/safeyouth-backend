from rest_framework import serializers

# Create your serializers here.

class Serializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
