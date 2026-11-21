from django.db import migrations


def remove_demo_products(apps, schema_editor):
    Product = apps.get_model("catalog", "Product")
    Product.objects.filter(is_demo=True).delete()


def restore_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [("catalog", "0001_initial")]
    operations = [migrations.RunPython(remove_demo_products, restore_noop)]
