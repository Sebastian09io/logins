# Generated by Django 5.0.4 on 2024-04-12 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laptops', '0005_alter_laptop_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laptop',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
