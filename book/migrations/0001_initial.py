# Generated by Django 5.2.3 on 2025-06-20 19:18

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Author",
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
                ("name", models.CharField(max_length=70)),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="images/"),
                ),
                ("biography", models.TextField()),
                ("builtIn", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=80)),
                ("builtIn", models.BooleanField(default=False)),
                ("sequence", models.IntegerField(default=1)),
            ],
            options={
                "ordering": ["sequence"],
            },
        ),
        migrations.CreateModel(
            name="Publisher",
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
                ("name", models.CharField(max_length=50)),
                ("builtIn", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Book",
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
                ("name", models.CharField(max_length=80)),
                (
                    "isbn",
                    models.CharField(
                        max_length=17,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Format must be 999-99-99999-99-9",
                                regex="^\\d{3}-\\d{2}-\\d{5}-\\d{2}-\\d$",
                            )
                        ],
                    ),
                ),
                ("pageCount", models.IntegerField(null=True)),
                (
                    "publishDate",
                    models.IntegerField(
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Format must be 2023", regex="^\\d{4}$"
                            )
                        ],
                    ),
                ),
                ("image", models.ImageField(null=True, upload_to="images/")),
                ("loanable", models.BooleanField(default=True)),
                (
                    "shelfCode",
                    models.CharField(
                        max_length=6,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Format must be AA-999",
                                regex="^[A-Za-z]{2}-\\d{3}$",
                            )
                        ],
                    ),
                ),
                ("active", models.BooleanField(default=True)),
                ("featured", models.BooleanField(default=False)),
                ("createDate", models.DateTimeField(default=django.utils.timezone.now)),
                ("builtIn", models.BooleanField(default=False)),
                ("authorId", models.ManyToManyField(to="book.author")),
                ("categoryId", models.ManyToManyField(to="book.category")),
                (
                    "publisherId",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="book.publisher"
                    ),
                ),
            ],
        ),
    ]
