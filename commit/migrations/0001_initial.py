# Generated by Django 4.2.1 on 2023-05-18 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("repository", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Commit",
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
                ("commit_msg", models.CharField(max_length=255)),
                ("commit_date", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
                ("is_rollback", models.BooleanField(default=False)),
                (
                    "repository_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.repository",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CommitFolder",
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
                ("folder_name", models.CharField(max_length=255)),
                (
                    "commit_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="commit.commit"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CommitFile",
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
                ("file_name", models.CharField(max_length=255)),
                (
                    "commit_folder_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="commit.commitfolder",
                    ),
                ),
                (
                    "commit_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="commit.commit"
                    ),
                ),
            ],
        ),
    ]
