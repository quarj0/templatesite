# Generated by Django 4.2 on 2023-07-11 10:41

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("templatesapi", "0004_userprofile_old_password"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="old_password",
        ),
    ]
