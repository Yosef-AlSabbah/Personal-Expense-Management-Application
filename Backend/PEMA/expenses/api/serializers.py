from rest_framework import serializers

from ..models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for displaying Category model details."""
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(help_text="The name of the category")
    description = serializers.CharField(required=False, allow_blank=True,
                                        help_text="Optional description of the category")

    class Meta:
        model = Category
        fields = ['id', 'name', 'description']
        read_only_fields = ['id', 'name', 'description']


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for Expense model with category association by ID only."""
    user = serializers.StringRelatedField(read_only=True, help_text="The user who owns this expense")
    category = CategorySerializer(read_only=True,
                                  help_text="Category details for this expense")  # Display only; not writable
    category_id = serializers.PrimaryKeyRelatedField(
        source='category',
        queryset=Category.objects.all(),
        write_only=True,
        required=True,
        help_text="Provide the ID of the existing category to associate with this expense."
    )
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Amount spent in the currency unit"
    )
    date = serializers.DateField(read_only=True, help_text="The date when the expense was recorded")
    description = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Optional description of the expense"
    )
    summary = serializers.CharField(
        read_only=True,
        help_text="Summary of the expense, for quick viewing"
    )

    class Meta:
        model = Expense
        fields = ['id', 'user', 'amount', 'date', 'category', 'category_id', 'description', 'summary']
        read_only_fields = ['id', 'user', 'date', 'summary']
        extra_kwargs = {
            'category': {'read_only': True}  # Ensures category is not in input fields
        }

    def validate_amount(self, value):
        """Ensure the amount is greater than zero."""
        if value <= 0:
            raise serializers.ValidationError("Expense amount must be greater than zero.")
        return value
