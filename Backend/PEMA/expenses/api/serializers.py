from rest_framework import serializers

from ..models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model, including ID, name, description, and title.
    """

    id = serializers.IntegerField(read_only=True, help_text="Unique identifier for the category.")
    name = serializers.CharField(help_text="The name of the category.")
    description = serializers.CharField(
        required=False, allow_blank=True, help_text="Optional description for the category."
    )
    title = serializers.CharField(read_only=True, help_text="Category title, same as the name.")

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'title']
        read_only_fields = ['title']


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Expense model, including details about the expense and nested category information.
    """
    user = serializers.StringRelatedField(
        read_only=True, help_text="The user who created this expense."
    )
    category = CategorySerializer(
        read_only=True, help_text="Nested category details for the expense."
    )
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True,
        required=True,
        help_text="ID of the category to associate with this expense."
    )
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, help_text="The amount of the expense. Must be greater than zero."
    )
    date = serializers.DateField(
        read_only=True, help_text="The date this expense was created."
    )
    description = serializers.CharField(
        required=False, allow_blank=True, help_text="Optional description of the expense."
    )
    summary = serializers.CharField(
        read_only=True, help_text="A summary description of the expense."
    )

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'date', 'category', 'category_id', 'description', 'summary']
        read_only_fields = ['id', 'user', 'date', 'summary']

    def validate_amount(self, value):
        """Ensure the expense amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be greater than zero.")
        return value
