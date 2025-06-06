# Generated by Django 3.2.16 on 2025-05-26 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_auto_20250521_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=57, unique=True, verbose_name='вопрос')),
                ('answer', models.CharField(max_length=1000, verbose_name='ответ')),
            ],
            options={
                'verbose_name': 'вопрос-ответ',
                'verbose_name_plural': 'FAQ',
            },
        ),
    ]
