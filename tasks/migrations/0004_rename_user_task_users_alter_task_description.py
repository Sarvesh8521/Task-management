# Generated by Django 4.2.20 on 2025-04-23 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_organization_super_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='user',
            new_name='users',
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(max_length=250),
        ),
    ]
