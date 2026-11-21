from django.db import migrations


def add_lights_category(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Category.objects.get_or_create(
        slug="lights",
        defaults={
            "name": "Lights",
            "description": "Lighting and everyday electrical essentials.",
            "accent": "orange",
            "is_active": True,
        },
    )


def remove_lights_category(apps, schema_editor):
    Category = apps.get_model("catalog", "Category")
    Category.objects.filter(slug="lights").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0002_remove_demo_products"),
    ]

    operations = [
        migrations.RunPython(add_lights_category, remove_lights_category),
    ]
