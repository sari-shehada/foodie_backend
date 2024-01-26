# Generated by Django 4.2.4 on 2024-01-26 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MealCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('subscriptionExpirationDate', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('phoneNumber', models.CharField(max_length=10, null=True)),
                ('landLine', models.CharField(max_length=7)),
                ('image', models.ImageField(upload_to='restaurants')),
            ],
        ),
    ]