# Generated by Django 5.0.6 on 2024-06-22 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseFirstChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nickname', models.CharField(max_length=255)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
