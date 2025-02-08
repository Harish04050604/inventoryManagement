# Generated by Django 5.1.6 on 2025-02-08 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_signup_designation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('ItemName', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('NumberOfItems', models.IntegerField()),
                ('SellingPrice', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
