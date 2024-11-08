from rest_framework import serializers
from ..models import Income


class IncomeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Income model, including all fields with best practices in mind.
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Income
        fields = ['user', 'amount', 'date', 'last_updated', 'description', 'summary']
        read_only_fields = ['user', 'date', 'last_updated', 'summary']

    def validate_amount(self, value):
        """
        Ensure the income amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Income amount must be greater than zero.")
        return value

    def to_representation(self, instance):
        """
        Custom representation to add a formatted description.
        """
        representation = super().to_representation(instance)
        representation['formatted_description'] = f"{instance.user} received {instance.amount} on {instance.date}"
        return representation
