# Generated by Django 5.0.6 on 2024-07-06 09:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_remove_transaction_subscription_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="organization",
            name="user_profile",
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="role",
            field=models.CharField(
                choices=[("student", "Student"), ("accountant", "Accountant")],
                max_length=20,
            ),
        ),
    ]
