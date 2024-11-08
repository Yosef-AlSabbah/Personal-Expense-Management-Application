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
    Serializer for the Expense model, including all fields with best practices in mind.
    """
    user = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Expense
        fields = ['user', 'amount', 'date', 'category', 'category_id', 'description', 'summary']
        read_only_fields = ['user', 'date', 'summary']

    def validate_amount(self, value):
        """
        Ensure the expense amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be greater than zero.")
        return value

    def to_representation(self, instance):
        """
        Custom representation to add a formatted description.
        """
        representation = super().to_representation(instance)
        representation['formatted_description'] = f"{instance.user} spent {instance.amount} in category {instance.category} on {instance.date}"
        return representation