from django.db import migrations


def add_lights_brand(apps, schema_editor):
    Brand = apps.get_model("catalog", "Brand")
    Brand.objects.get_or_create(
        slug="lights",
        defaults={"name": "Lights", "is_active": True},
    )


def remove_lights_brand(apps, schema_editor):
    Brand = apps.get_model("catalog", "Brand")
    Brand.objects.filter(slug="lights").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0004_add_bulbs_category"),
    ]

    operations = [
        migrations.RunPython(add_lights_brand, remove_lights_brand),
    ]
