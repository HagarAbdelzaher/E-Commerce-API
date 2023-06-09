# Generated by Django 4.2 on 2023-05-20 00:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0002_alter_order_options_order_stripe_token"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="payment_method",
        ),
        migrations.RemoveField(
            model_name="order",
            name="stripe_token",
        ),
        migrations.AddField(
            model_name="order",
            name="payment_status",
            field=models.CharField(
                choices=[("paid", "Paid"), ("unpaid", "Unpaid")],
                default="unpaid",
                max_length=10,
            ),
        ),
    ]
