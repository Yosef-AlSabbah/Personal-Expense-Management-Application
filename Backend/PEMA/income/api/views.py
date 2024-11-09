from rest_framework.generics import RetrieveUpdateAPIView

from .serializers import IncomeSerializer
from ..models import Income


class CreateOrUpdateIncomeView(RetrieveUpdateAPIView):
    """
    API view to create or update an Income entry for the authenticated user.
    If an Income entry exists, it will be updated; otherwise, a new entry will be created.
    """
    serializer_class = IncomeSerializer

    def get_object(self):
        """
        Retrieves the Income object for the authenticated user, creating it if it does not exist.
        """
        user = self.request.user
        income, created = Income.objects.get_or_create(user=user)
        return income
