# Generated by Django 5.2.3 on 2025-06-10 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_plan_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='amount',
            field=models.DecimalField(decimal_places=7, max_digits=12),
        ),
        migrations.AlterField(
            model_name='plan',
            name='roi',
            field=models.DecimalField(decimal_places=2, default=50, max_digits=12),
        ),
        migrations.AlterField(
            model_name='plan',
            name='time',
            field=models.DecimalField(decimal_places=2, default=7, max_digits=12),
        ),
    ]
