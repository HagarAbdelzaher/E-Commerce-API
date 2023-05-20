# Generated by Django 4.2 on 2023-05-20 15:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0003_remove_order_payment_method_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="payment_status",
        ),
        migrations.AddField(
            model_name="order",
            name="paid",
            field=models.BooleanField(default=False),
        ),
    ]
