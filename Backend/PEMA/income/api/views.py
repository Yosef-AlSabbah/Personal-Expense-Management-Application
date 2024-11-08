from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView

from .serializers import IncomeSerializer
from ..models import Income


class CreateIncomeView(CreateAPIView):
    """
    View to create a new Income entry for the authenticated user.
    Ensures that the user does not already have an income entry.
    """
    serializer_class = IncomeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        # Check if an Income instance already exists for the user
        if Income.objects.filter(user=user).exists():
            raise ValidationError("Income entry already exists for this user.")
        # Save the new income entry with the user set
        serializer.save(user=user)


class UpdateIncomeView(UpdateAPIView):
    """
    View to update an existing Income entry for the authenticated user.
    Ensures that an income entry exists before updating.
    """
    serializer_class = IncomeSerializer

    def get_object(self):
        user = self.request.user
        try:
            # Retrieve the existing Income instance for the user
            return Income.objects.get(user=user)
        except Income.DoesNotExist:
            raise ValidationError("Income entry does not exist for this user.")
