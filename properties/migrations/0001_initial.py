# Generated by Django 5.2 on 2025-05-13 12:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sellers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('street_address', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True)),
                ('size', models.IntegerField(help_text='Size in square meters')),
                ('price', models.IntegerField(help_text='Price in ISK')),
                ('rooms', models.IntegerField()),
                ('bedrooms', models.IntegerField(default=0)),
                ('bathrooms', models.IntegerField()),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Sold', 'Sold')], default='Available', max_length=50)),
                ('type', models.CharField(choices=[('House', 'House'), ('Apartment', 'Apartment'), ('Villa', 'Villa'), ('Townhouse', 'Townhouse'), ('Sumarhús', 'Sumarhús'), ('Fjölbýlishús', 'Fjölbýlishús'), ('Einbýlishús', 'Einbýlishús')], max_length=100)),
                ('date_listed', models.DateField(blank=True, null=True)),
                ('description', models.TextField()),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='sellers.seller')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='properties/images')),
                ('order', models.PositiveIntegerField(default=0)),
                ('related_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='properties.property')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
