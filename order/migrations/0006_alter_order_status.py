# Generated by Django 4.2 on 2023-05-24 00:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0005_alter_order_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "pending"),
                    ("shipped", "shipped"),
                    ("delivered", "delivered"),
                    ("canceled", "canceled"),
                ],
                default="pending",
                max_length=10,
            ),
        ),
    ]
