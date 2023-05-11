# Generated by Django 4.2 on 2023-05-09 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("category", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20, unique=True)),
                (
                    "image",
                    models.CharField(blank=True, default="", max_length=200, null=True),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("description", models.CharField(max_length=100)),
                ("quantity", models.IntegerField()),
                (
                    "category_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="category.category",
                    ),
                ),
            ],
        ),
    ]
