# Generated by Django 5.0.7 on 2024-08-15 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_alter_item_unique_together_item_available_dates_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='available_dates',
            field=models.TextField(blank=True, null=True),
        ),
    ]
