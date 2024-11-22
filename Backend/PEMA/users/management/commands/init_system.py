from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Initialize the system by creating default categories and a superuser."

    def handle(self, *args, **kwargs):
        from expenses.models import Category
        from django.contrib.auth import get_user_model  # Dynamically retrieve the User model

        User = get_user_model()

        # Step 1: Create predefined categories
        categories = [
            {"name": "Rent", "description": "Monthly or regular payments for housing or office spaces."},
            {"name": "Medical",
             "description": "Medical-related expenses, including doctor's visits, medication, therapy, and hospital fees."},
            {"name": "Food", "description": "Expenses for meals, groceries, snacks, and dining out."},
            {"name": "Transportation",
             "description": "Costs related to getting from one place to another, such as bus fares, taxi rides, or fuel expenses."},
        ]

        self.stdout.write("Initializing categories...")
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data["name"],
                defaults={"description": category_data["description"]},
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            else:
                self.stdout.write(f"Category already exists: {category.name}")

        # Step 2: Create the superuser
        self.stdout.write("Creating superuser...")
        email = "yalsabbah@students.iugaza.edu.ps"
        password = "0"
        phone_number = "+972598129670"
        first_name = "Yousef"
        last_name = "Al Sabbah"

        if not User.objects.filter(email=email).exists():
            superuser = User.objects.create_superuser(
                email=email,
                password=password,
                username="Admin",
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser created: {superuser.email}"))
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists."))

        self.stdout.write(self.style.SUCCESS("System initialization complete."))
