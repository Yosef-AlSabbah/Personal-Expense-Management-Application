from rest_framework.generics import CreateAPIView

from .serializers import ExpenseSerializer
from ..models import Expense


class ExpenseCreateView(CreateAPIView):
    """
    API view to create a new Expense entry.
    Only authenticated users are permitted to create new Expense records.
    """
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    def perform_create(self, serializer):
        """
        Assigns the authenticated user as the owner of the expense entry upon creation.
        """
        serializer.save(user=self.request.user)
