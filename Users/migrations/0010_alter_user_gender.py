# Generated by Django 5.2 on 2025-04-23 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0009_remove_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], null=True, verbose_name='Género'),
        ),
    ]
