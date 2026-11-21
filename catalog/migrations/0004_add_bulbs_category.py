from django.db import migrations


def add_bulbs_category(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Category.objects.get_or_create(
        slug="bulbs",
        defaults={
            "name": "Bulbs",
            "description": "LED bulbs and everyday lighting products.",
            "accent": "orange",
            "is_active": True,
        },
    )


def remove_bulbs_category(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Category.objects.filter(slug="bulbs").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_add_lights_category"),
    ]

    operations = [
        migrations.RunPython(add_bulbs_category, remove_bulbs_category),
    ]
