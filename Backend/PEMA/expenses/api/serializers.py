from rest_framework import serializers
from ..models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model, including all fields with best practices in mind.
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'title']
        read_only_fields = ['title']


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Expense model, including all necessary fields and following best practices.
    """
    user = serializers.StringRelatedField(read_only=True)

    # Nested serializer for category details
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'date', 'category', 'description', 'summary']
        read_only_fields = ['id', 'user', 'date', 'summary']

    def validate_amount(self, value):
        """
        Ensure the expense amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be greater than zero.")
        return value
