# Generated by Django 4.2.5 on 2023-11-28 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_diaryentry_user_task_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]