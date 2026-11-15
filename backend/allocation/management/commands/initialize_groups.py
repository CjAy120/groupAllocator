
from django.core.management.base import BaseCommand

from allocation.models import Group


class Command(BaseCommand):
    help = "Create or update the 18 student allocation groups."

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for number in range(1, 19):
            capacity = 4 if number <= 16 else 3

            group, created = Group.objects.update_or_create(
                number=number,
                defaults={"capacity": capacity},
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Group initialization complete. "
                f"Created: {created_count}, updated: {updated_count}."
            )
        )
