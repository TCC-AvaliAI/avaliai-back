# Generated by Django 5.1.7 on 2025-04-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam',
            name='difficulty',
            field=models.CharField(choices=[('EASY', 'Fácil'), ('MEDIUM', 'Média'), ('HARD', 'Difícil')], default='MEDIUM', max_length=20),
        ),
    ]
