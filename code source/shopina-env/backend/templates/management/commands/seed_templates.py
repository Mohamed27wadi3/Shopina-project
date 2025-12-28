from django.core.management.base import BaseCommand
from templates.models import Template


SAMPLE_TEMPLATES = [
    {
        "title": "Nova",
        "category": "Minimal",
        "image": "https://picsum.photos/seed/nova/640/400",
        "description": "Template minimal clair",
        "is_active": True,
    },
    {
        "title": "Aero",
        "category": "Fashion",
        "image": "https://picsum.photos/seed/aero/640/400",
        "description": "Style fashion pour vêtements",
        "is_active": True,
    },
    {
        "title": "Mercury",
        "category": "Electronics",
        "image": "https://picsum.photos/seed/mercury/640/400",
        "description": "Template orienté tech",
        "is_active": True,
    },
]


class Command(BaseCommand):
    help = "Seed sample templates for the marketplace"

    def handle(self, *args, **options):
        created = 0
        for data in SAMPLE_TEMPLATES:
            obj, is_created = Template.objects.get_or_create(
                title=data["title"],
                defaults=data,
            )
            created += 1 if is_created else 0
        total = Template.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Seed ok. Created: {created}. Total templates: {total}"))
