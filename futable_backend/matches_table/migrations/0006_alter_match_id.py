# Generated by Django 5.1.4 on 2025-01-03 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches_table', '0005_alter_match_id_alter_match_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
