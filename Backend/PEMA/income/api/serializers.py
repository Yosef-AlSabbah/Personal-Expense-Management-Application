from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from ..models import Income


class IncomeSerializer(ModelSerializer):
    """
    Serializer for the Income model, including all fields with validation.
    """
    user = serializers.StringRelatedField(
        read_only=True,
        help_text="The user to whom this income entry belongs."
    )
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The amount of income. Must be greater than zero.",
    )
    date = serializers.DateField(
        read_only=True,
        help_text="The date this income entry was created."
    )
    last_updated = serializers.DateTimeField(
        read_only=True,
        help_text="The timestamp when this income entry was last updated."
    )
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="A description or note for the income entry."
    )
    summary = serializers.CharField(
        read_only=True,
        help_text="A brief summary of the income entry."
    )

    class Meta:
        model = Income
        fields = ['user', 'amount', 'date', 'last_updated', 'description', 'summary']
        read_only_fields = ['user', 'date', 'last_updated', 'summary']

    def validate_amount(self, value):
        """Ensure the income amount is positive."""
        if value <= 0:
            raise ValidationError("Income amount must be greater than zero.")
        return value
